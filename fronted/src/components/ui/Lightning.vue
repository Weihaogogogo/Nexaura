<template>
  <canvas 
    ref="canvasRef" 
    class="w-full h-full relative"
  ></canvas>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'

interface LightningProps {
  hue?: number
  xOffset?: number
  speed?: number
  intensity?: number
  size?: number
}

const props = withDefaults(defineProps<LightningProps>(), {
  hue: 230,
  xOffset: 0,
  speed: 1,
  intensity: 1,
  size: 1
})

const canvasRef = ref<HTMLCanvasElement | null>(null)
let animationId: number | null = null
let gl: WebGLRenderingContext | null = null
let program: WebGLProgram | null = null
let startTime: number = 0

// Uniform locations
let iResolutionLocation: WebGLUniformLocation | null = null
let iTimeLocation: WebGLUniformLocation | null = null
let uHueLocation: WebGLUniformLocation | null = null
let uXOffsetLocation: WebGLUniformLocation | null = null
let uSpeedLocation: WebGLUniformLocation | null = null
let uIntensityLocation: WebGLUniformLocation | null = null
let uSizeLocation: WebGLUniformLocation | null = null

const vertexShaderSource = `
  attribute vec2 aPosition;
  void main() {
    gl_Position = vec4(aPosition, 0.0, 1.0);
  }
`

const fragmentShaderSource = `
  precision mediump float;
  uniform vec2 iResolution;
  uniform float iTime;
  uniform float uHue;
  uniform float uXOffset;
  uniform float uSpeed;
  uniform float uIntensity;
  uniform float uSize;
  
  #define OCTAVE_COUNT 10

  // Convert HSV to RGB.
  vec3 hsv2rgb(vec3 c) {
      vec3 rgb = clamp(abs(mod(c.x * 6.0 + vec3(0.0,4.0,2.0), 6.0) - 3.0) - 1.0, 0.0, 1.0);
      return c.z * mix(vec3(1.0), rgb, c.y);
  }

  float hash11(float p) {
      p = fract(p * .1031);
      p *= p + 33.33;
      p *= p + p;
      return fract(p);
  }

  float hash12(vec2 p) {
      vec3 p3 = fract(vec3(p.xyx) * .1031);
      p3 += dot(p3, p3.yzx + 33.33);
      return fract((p3.x + p3.y) * p3.z);
  }

  mat2 rotate2d(float theta) {
      float c = cos(theta);
      float s = sin(theta);
      return mat2(c, -s, s, c);
  }

  float noise(vec2 p) {
      vec2 ip = floor(p);
      vec2 fp = fract(p);
      float a = hash12(ip);
      float b = hash12(ip + vec2(1.0, 0.0));
      float c = hash12(ip + vec2(0.0, 1.0));
      float d = hash12(ip + vec2(1.0, 1.0));
      
      vec2 t = smoothstep(0.0, 1.0, fp);
      return mix(mix(a, b, t.x), mix(c, d, t.x), t.y);
  }

  float fbm(vec2 p) {
      float value = 0.0;
      float amplitude = 0.5;
      for (int i = 0; i < OCTAVE_COUNT; ++i) {
          value += amplitude * noise(p);
          p *= rotate2d(0.45);
          p *= 2.0;
          amplitude *= 0.5;
      }
      return value;
  }

  void mainImage( out vec4 fragColor, in vec2 fragCoord ) {
      // Normalized pixel coordinates.
      vec2 uv = fragCoord / iResolution.xy;
      uv = 2.0 * uv - 1.0;
      uv.x *= iResolution.x / iResolution.y;
      // Apply horizontal offset.
      uv.x += uXOffset;
      
      // Adjust uv based on size and animate with speed.
      uv += 2.0 * fbm(uv * uSize + 0.8 * iTime * uSpeed) - 1.0;
      
      float dist = abs(uv.x);
      // Compute base color using hue.
      vec3 baseColor = hsv2rgb(vec3(uHue / 360.0, 0.7, 0.8));
      // Compute color with intensity and speed affecting time.
      vec3 col = baseColor * pow(mix(0.0, 0.07, hash11(iTime * uSpeed)) / dist, 1.0) * uIntensity;
      col = pow(col, vec3(1.0));
      fragColor = vec4(col, 1.0);
  }

  void main() {
      mainImage(gl_FragColor, gl_FragCoord.xy);
  }
`

const compileShader = (source: string, type: number): WebGLShader | null => {
  if (!gl) return null
  
  const shader = gl.createShader(type)
  if (!shader) return null
  
  gl.shaderSource(shader, source)
  gl.compileShader(shader)
  
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    console.error('Shader compile error:', gl.getShaderInfoLog(shader))
    gl.deleteShader(shader)
    return null
  }
  
  return shader
}

const resizeCanvas = () => {
  const canvas = canvasRef.value
  if (!canvas) return
  
  canvas.width = canvas.clientWidth
  canvas.height = canvas.clientHeight
}

const render = () => {
  const canvas = canvasRef.value
  if (!canvas || !gl || !program) return
  
  resizeCanvas()
  gl.viewport(0, 0, canvas.width, canvas.height)
  
  if (iResolutionLocation) {
    gl.uniform2f(iResolutionLocation, canvas.width, canvas.height)
  }
  
  const currentTime = performance.now()
  if (iTimeLocation) {
    gl.uniform1f(iTimeLocation, (currentTime - startTime) / 1000.0)
  }
  
  if (uHueLocation) {
    gl.uniform1f(uHueLocation, props.hue)
  }
  
  if (uXOffsetLocation) {
    gl.uniform1f(uXOffsetLocation, props.xOffset)
  }
  
  if (uSpeedLocation) {
    gl.uniform1f(uSpeedLocation, props.speed)
  }
  
  if (uIntensityLocation) {
    gl.uniform1f(uIntensityLocation, props.intensity)
  }
  
  if (uSizeLocation) {
    gl.uniform1f(uSizeLocation, props.size)
  }
  
  gl.drawArrays(gl.TRIANGLES, 0, 6)
  animationId = requestAnimationFrame(render)
}

const initWebGL = () => {
  const canvas = canvasRef.value
  if (!canvas) return
  
  resizeCanvas()
  
  gl = canvas.getContext('webgl')
  if (!gl) {
    console.error('WebGL not supported')
    return
  }
  
  const vertexShader = compileShader(vertexShaderSource, gl.VERTEX_SHADER)
  const fragmentShader = compileShader(fragmentShaderSource, gl.FRAGMENT_SHADER)
  
  if (!vertexShader || !fragmentShader) return
  
  program = gl.createProgram()
  if (!program) return
  
  gl.attachShader(program, vertexShader)
  gl.attachShader(program, fragmentShader)
  gl.linkProgram(program)
  
  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    console.error('Program linking error:', gl.getProgramInfoLog(program))
    return
  }
  
  gl.useProgram(program)
  
  const vertices = new Float32Array([
    -1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1,
  ])
  
  const vertexBuffer = gl.createBuffer()
  gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer)
  gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW)
  
  const aPosition = gl.getAttribLocation(program, 'aPosition')
  gl.enableVertexAttribArray(aPosition)
  gl.vertexAttribPointer(aPosition, 2, gl.FLOAT, false, 0, 0)
  
  // Get uniform locations
  iResolutionLocation = gl.getUniformLocation(program, 'iResolution')
  iTimeLocation = gl.getUniformLocation(program, 'iTime')
  uHueLocation = gl.getUniformLocation(program, 'uHue')
  uXOffsetLocation = gl.getUniformLocation(program, 'uXOffset')
  uSpeedLocation = gl.getUniformLocation(program, 'uSpeed')
  uIntensityLocation = gl.getUniformLocation(program, 'uIntensity')
  uSizeLocation = gl.getUniformLocation(program, 'uSize')
  
  startTime = performance.now()
  render()
}

onMounted(() => {
  initWebGL()
  window.addEventListener('resize', resizeCanvas)
})

onUnmounted(() => {
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
  window.removeEventListener('resize', resizeCanvas)
})

// Watch for prop changes that should trigger re-rendering
watch([() => props.hue, () => props.xOffset, () => props.speed, () => props.intensity, () => props.size], () => {
  // The render loop will automatically pick up the new values
})
</script>

<style scoped>
canvas {
  display: block;
}
</style> 