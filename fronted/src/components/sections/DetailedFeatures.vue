<template>
  <div class="detailed-features">
    <!-- Detailed Features Section -->
    <section id="detailed-features" class="feature-section section">
      <div class="container">
        <div class="section-label">SEO Content Platform</div>
        <h2 class="section-title">
          Discover the simplicity of content creation with our AI-powered platform
        </h2>

        <div class="features-grid">
          <div class="feature-item">
            <div class="feature-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
              </svg>
            </div>
            <h3 class="feature-title">Smart Article Editor</h3>
            <p class="feature-description">
              Crafting your stories with our ultra-simple article editor, designed for seamless AI writing and editing.
            </p>
          </div>

          <div class="feature-item">
            <div class="feature-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6zm16-4H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-1 9H9V9h10v2zm-4 4H9v-2h6v2zm4-8H9V5h10v2z"/>
              </svg>
            </div>
            <h3 class="feature-title">7-Step Workflow</h3>
            <p class="feature-description">
              Quickly design your content strategy with our intuitive step-by-step process, making SEO optimization a breeze.
            </p>
          </div>

          <div class="feature-item">
            <div class="feature-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96z"/>
              </svg>
            </div>
            <h3 class="feature-title">AI-Powered Research</h3>
            <p class="feature-description">
              Advanced AI research capabilities, ensuring your content is well-researched and competitive.
            </p>
          </div>

          <div class="feature-item">
            <div class="feature-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm-1 16H9V7h9v14z"/>
              </svg>
            </div>
            <h3 class="feature-title">Content Optimization</h3>
            <p class="feature-description">
              Real-time SEO optimization and content analysis to maximize your search engine visibility.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- AI Writing Section -->
    <section class="ai-writing-section section">
      <div class="container">
        <div class="section-content">
          <div class="content-left">
            <div class="section-label">AI Writing</div>
            <h2 class="section-title">
              Professional content creation at scale
            </h2>
            <p class="section-description">
              Our AI understands context, tone, and SEO requirements to create content that resonates with your audience and ranks well in search engines.
            </p>
            <div class="features-list">
              <div class="feature-point">
                <div class="check-icon">✓</div>
                <span>Keyword research and optimization</span>
              </div>
              <div class="feature-point">
                <div class="check-icon">✓</div>
                <span>Content structure planning</span>
              </div>
              <div class="feature-point">
                <div class="check-icon">✓</div>
                <span>Real-time SEO scoring</span>
              </div>
            </div>
          </div>
          <div class="content-right">
            <div class="demo-preview">
              <div class="preview-header">
                <div class="preview-dots">
                  <div class="dot"></div>
                  <div class="dot"></div>
                  <div class="dot"></div>
                </div>
                <span class="preview-title">Article Generator</span>
              </div>
              <div class="preview-content">
                <div class="step-indicator">
                  <div class="step active">1. Keywords</div>
                  <div class="step active">2. Analysis</div>
                  <div class="step active">3. Topic</div>
                  <div class="step">4. Title</div>
                </div>
                <div class="content-area">
                  <div class="typing-animation">Generating SEO-optimized content...</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.detailed-features {
  background: #fafbff;
}

.feature-section {
  padding: 4rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.section {
  padding: 4rem 0;
}

.section-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #6366f1;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 1rem;
  text-align: center;
}

.section-title {
  font-size: 2.25rem;
  font-weight: 600;
  color: #1e1b4b;
  text-align: center;
  margin-bottom: 3rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
}

.feature-item {
  text-align: center;
  padding: 2rem 1rem;
}

.feature-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border-radius: 50%;
  color: white;
  margin-bottom: 1.5rem;
}

.feature-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e1b4b;
  margin-bottom: 1rem;
}

.feature-description {
  font-size: 1rem;
  color: #64748b;
  line-height: 1.6;
}

/* AI Writing Section */
.ai-writing-section {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
}

.section-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.content-left .section-label {
  text-align: left;
}

.content-left .section-title {
  text-align: left;
  margin-bottom: 1.5rem;
}

.section-description {
  font-size: 1.125rem;
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.features-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.feature-point {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.check-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background: #10b981;
  color: white;
  border-radius: 50%;
  font-weight: bold;
  font-size: 0.875rem;
}

/* Demo Preview */
.demo-preview {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 0.75rem;
  overflow: hidden;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.preview-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
}

.preview-dots {
  display: flex;
  gap: 0.5rem;
}

.dot {
  width: 12px;
  height: 12px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
}

.preview-title {
  font-weight: 500;
}

.preview-content {
  padding: 1.5rem;
}

.step-indicator {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.step {
  padding: 0.5rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  background: #f1f5f9;
  color: #64748b;
}

.step.active {
  background: #6366f1;
  color: white;
}

.content-area {
  background: #f8fafc;
  border-radius: 0.5rem;
  padding: 1.5rem;
  min-height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.typing-animation {
  color: #6366f1;
  font-weight: 500;
  position: relative;
}

.typing-animation::after {
  content: '|';
  animation: blink 1s infinite;
  margin-left: 0.25rem;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

@media (max-width: 768px) {
  .section-content {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .features-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .section-title {
    font-size: 1.875rem;
  }

  .feature-item {
    padding: 1.5rem 1rem;
  }
}
</style>