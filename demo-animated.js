/**
 * Animated Video Demo Controller
 * Creates a video-like experience using CSS animations and JavaScript
 */

class AnimatedDemoVideo {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error('Demo video container not found');
            return;
        }

        this.currentSlide = 0;
        this.isPlaying = false;
        this.slideDuration = 5000; // 5 seconds per slide
        this.slides = this.createSlides();
        this.timer = null;
        this.totalDuration = this.slides.length * this.slideDuration;

        this.init();
    }

    createSlides() {
        return [
            {
                id: 'intro',
                type: 'intro',
                duration: 4000,
                render: () => `
                    <div class="demo-video-slide slide-intro active">
                        <div class="logo">🤖</div>
                        <h1>Bharat GST AI</h1>
                        <p>India's #1 Automated GST Return Assistant</p>
                        <div style="margin-top: 40px; display: flex; gap: 20px; justify-content: center; flex-wrap: wrap;">
                            <div style="background: rgba(255,255,255,0.1); padding: 15px 25px; border-radius: 10px;">
                                <div style="font-size: 2rem; font-weight: 700; color: #00f2fe;">140M+</div>
                                <div style="font-size: 0.9rem; opacity: 0.8;">GST Users</div>
                            </div>
                            <div style="background: rgba(255,255,255,0.1); padding: 15px 25px; border-radius: 10px;">
                                <div style="font-size: 2rem; font-weight: 700; color: #00f2fe;">95%</div>
                                <div style="font-size: 0.9rem; opacity: 0.8;">Accuracy</div>
                            </div>
                        </div>
                    </div>
                `
            },
            {
                id: 'problem',
                type: 'problem',
                duration: 5000,
                render: () => `
                    <div class="demo-video-slide slide-problem active">
                        <h2 style="font-size: 2.5rem; margin-bottom: 10px; color: #d63031;">😫 The GST Nightmare!</h2>
                        <p style="font-size: 1.3rem; color: rgba(255,255,255,0.8);">Businesses are losing thousands every month</p>
                        <div class="pain-points">
                            <div class="pain-point">
                                <i class="fas fa-clock"></i>
                                <h3>30+ Hours/Month</h3>
                                <p>Hours wasted on manual GST filing</p>
                            </div>
                            <div class="pain-point">
                                <i class="fas fa-exclamation-triangle"></i>
                                <h3>₹50K Penalties</h3>
                                <p>Lost due to missed deadlines</p>
                            </div>
                            <div class="pain-point">
                                <i class="fas fa-file-invoice"></i>
                                <h3>Manual Errors</h3>
                                <p>Wrong calculations cause big losses</p>
                            </div>
                        </div>
                    </div>
                `
            },
            {
                id: 'solution',
                type: 'solution',
                duration: 6000,
                render: () => `
                    <div class="demo-video-slide slide-solution active">
                        <h2 style="font-size: 2.5rem; margin-bottom: 10px; color: #00f2fe;">✨ AI-Powered Solution!</h2>
                        <p style="font-size: 1.3rem; color: rgba(255,255,255,0.8);">Automate everything in 60 seconds</p>
                        <div class="features-grid">
                            <div class="feature-card">
                                <i class="fas fa-calculator"></i>
                                <h3>Auto GST Calc</h3>
                                <p>Instant CGST/SGST/IGST</p>
                            </div>
                            <div class="feature-card">
                                <i class="fas fa-file-pdf"></i>
                                <h3>PDF Invoices</h3>
                                <p>Professional & GST-compliant</p>
                            </div>
                            <div class="feature-card">
                                <i class="fas fa-chart-bar"></i>
                                <h3>GSTR Reports</h3>
                                <p>One-click GSTR-1/3B/9</p>
                            </div>
                            <div class="feature-card">
                                <i class="fas fa-bell"></i>
                                <h3>Smart Reminders</h3>
                                <p>Never miss a deadline</p>
                            </div>
                        </div>
                    </div>
                `
            },
            {
                id: 'gst-calc',
                type: 'gst',
                duration: 5000,
                render: () => `
                    <div class="demo-video-slide slide-gst active">
                        <div class="content-wrapper" style="display: flex; align-items: center; justify-content: center; width: 100%;">
                            <div class="gst-display">
                                <div style="font-size: 1.2rem; margin-bottom: 10px; color: rgba(255,255,255,0.8);">Example Invoice Amount</div>
                                <div class="amount">₹10,000</div>
                                <div style="font-size: 1.1rem; color: rgba(255,255,255,0.7); margin-bottom: 20px;">@ 18% GST Rate</div>
                                <div class="gst-breakdown">
                                    <div class="gst-item">
                                        <h4>CGST</h4>
                                        <div class="value">₹900</div>
                                    </div>
                                    <div class="gst-item">
                                        <h4>SGST</h4>
                                        <div class="value">₹900</div>
                                    </div>
                                    <div class="gst-item">
                                        <h4>Total</h4>
                                        <div class="value">₹11,800</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                `
            },
            {
                id: 'pdf-gen',
                type: 'pdf',
                duration: 5000,
                render: () => `
                    <div class="demo-video-slide slide-pdf active">
                        <h2 style="font-size: 2.5rem; margin-bottom: 10px; color: #00b894;">📄 Professional PDF Invoice</h2>
                        <p style="font-size: 1.3rem; color: rgba(255,255,255,0.8);">Generate GST-compliant invoices in 1 click</p>
                        <div class="pdf-animation">
                            <div class="pdf-preview">
                                <div class="invoice-header"></div>
                                <div class="invoice-lines">
                                    <div class="line long"></div>
                                    <div class="line medium"></div>
                                    <div class="line medium"></div>
                                    <div class="line short"></div>
                                    <div class="line long"></div>
                                </div>
                            </div>
                            <div class="success-animation">
                                <div class="check">✅</div>
                                <h3 style="color: #00b894; font-size: 1.8rem; margin-bottom: 10px;">Generated!</h3>
                                <p style="color: rgba(255,255,255,0.8); font-size: 1.1rem;">Ready to download & share</p>
                            </div>
                        </div>
                    </div>
                `
            },
            {
                id: 'gstr',
                type: 'gstr',
                duration: 6000,
                render: () => `
                    <div class="demo-video-slide slide-gstr active">
                        <h2 style="font-size: 2.5rem; margin-bottom: 10px; color: #00f2fe;">📊 GSTR Returns Ready!</h2>
                        <p style="font-size: 1.3rem; color: rgba(255,255,255,0.8);">Auto-generated and ready to file</p>
                        <div class="gstr-cards">
                            <div class="gstr-card">
                                <i class="fas fa-file-alt"></i>
                                <h3>GSTR-1</h3>
                                <div class="status">✓ Updated</div>
                            </div>
                            <div class="gstr-card">
                                <i class="fas fa-file-alt"></i>
                                <h3>GSTR-3B</h3>
                                <div class="status">✓ Ready</div>
                            </div>
                            <div class="gstr-card">
                                <i class="fas fa-bell"></i>
                                <h3>Reminder</h3>
                                <div class="status" style="font-size: 1.2rem;">20th March</div>
                            </div>
                        </div>
                        <div class="time-saved">
                            ⚡ Time Saved: 90% | Manual: 30min → AI: 3min
                        </div>
                    </div>
                `
            },
            {
                id: 'cta',
                type: 'cta',
                duration: 5000,
                render: () => `
                    <div class="demo-video-slide slide-cta active">
                        <h2>Ready to Automate Your GST?</h2>
                        <p style="font-size: 1.3rem; opacity: 0.9; max-width: 600px; margin: 0 auto 20px;">
                            Join 140M+ businesses already saving thousands with AI automation
                        </p>
                        <div style="display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; margin-bottom: 30px;">
                            <div style="background: rgba(255,255,255,0.2); padding: 15px 30px; border-radius: 10px;">
                                <div style="font-size: 1.5rem; font-weight: 700;">₹999</div>
                                <div style="font-size: 0.8rem;">Starting Plan</div>
                            </div>
                            <div style="background: rgba(0,184,148,0.2); padding: 15px 30px; border-radius: 10px;">
                                <div style="font-size: 1.5rem; font-weight: 700; color: #00b894;">Save ₹50K</div>
                                <div style="font-size: 0.8rem;">Annual Savings</div>
                            </div>
                        </div>
                        <a href="#" class="cta-button" onclick="alert('Thank you for your interest! Sales team will contact you soon.'); return false;">
                            <i class="fab fa-github" style="margin-right: 10px;"></i>
                            Start Free Trial
                        </a>
                    </div>
                `
            }
        ];
    }

    init() {
        this.renderContainer();
        this.setupControls();
        this.renderSlide(0);
    }

    renderContainer() {
        this.container.innerHTML = `
            <div class="demo-video-container">
                <div class="demo-video-player" id="demoVideoPlayer"></div>
                <div class="demo-video-controls">
                    <button class="play-btn" id="playPauseBtn">
                        <i class="fas fa-play"></i>
                    </button>
                    <div class="progress-bar">
                        <div class="progress-fill" id="progressFill"></div>
                    </div>
                    <div class="time-display" id="timeDisplay">0:00 / 0:35</div>
                    <div class="slide-number" id="slideNumber">1 / ${this.slides.length}</div>
                </div>
            </div>
        `;
    }

    renderSlide(index) {
        const player = document.getElementById('demoVideoPlayer');
        const slide = this.slides[index];

        // Remove active class from current slide
        const currentSlide = player.querySelector('.active');
        if (currentSlide) {
            currentSlide.classList.remove('active');
            currentSlide.classList.add('exiting');
            setTimeout(() => {
                currentSlide.remove();
            }, 800);
        }

        // Add new slide
        setTimeout(() => {
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = slide.render().trim();
            const newSlide = tempDiv.firstChild;
            player.appendChild(newSlide);

            // Small delay to trigger transition
            setTimeout(() => {
                newSlide.classList.add('active');
            }, 50);
        }, 300);

        // Update UI
        this.updateSlideNumber();
    }

    setupControls() {
        const playPauseBtn = document.getElementById('playPauseBtn');

        playPauseBtn.addEventListener('click', () => {
            this.togglePlay();
        });
    }

    togglePlay() {
        this.isPlaying = !this.isPlaying;
        const playPauseBtn = document.getElementById('playPauseBtn');
        playPauseBtn.innerHTML = this.isPlaying ?
            '<i class="fas fa-pause"></i>' :
            '<i class="fas fa-play"></i>';

        if (this.isPlaying) {
            this.startPlayback();
        } else {
            this.stopPlayback();
        }
    }

    startPlayback() {
        const slide = this.slides[this.currentSlide];
        this.timer = setInterval(() => {
            this.nextSlide();
        }, slide.duration);
    }

    stopPlayback() {
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
    }

    nextSlide() {
        this.currentSlide = (this.currentSlide + 1) % this.slides.length;
        this.renderSlide(this.currentSlide);
        this.updateProgress();

        // Restart timer with new slide duration
        if (this.isPlaying) {
            this.stopPlayback();
            this.startPlayback();
        }
    }

    previousSlide() {
        this.currentSlide = (this.currentSlide - 1 + this.slides.length) % this.slides.length;
        this.renderSlide(this.currentSlide);
        this.updateProgress();

        if (this.isPlaying) {
            this.stopPlayback();
            this.startPlayback();
        }
    }

    updateProgress() {
        const progressFill = document.getElementById('progressFill');
        const progress = ((this.currentSlide + 1) / this.slides.length) * 100;
        progressFill.style.width = `${progress}%`;

        const currentTime = this.calculateCurrentTime();
        const totalTime = this.calculateTotalTime();
        const timeDisplay = document.getElementById('timeDisplay');
        timeDisplay.textContent = `${this.formatTime(currentTime)} / ${this.formatTime(totalTotalTime)}`;
    }

    calculateCurrentTime() {
        let time = 0;
        for (let i = 0; i < this.currentSlide; i++) {
            time += this.slides[i].duration;
        }
        return time;
    }

    calculateTotalTime() {
        return this.slides.reduce((total, slide) => total + slide.duration, 0);
    }

    updateSlideNumber() {
        const slideNumber = document.getElementById('slideNumber');
        slideNumber.textContent = `${this.currentSlide + 1} / ${this.slides.length}`;
    }

    formatTime(ms) {
        const seconds = Math.floor(ms / 1000);
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    }
}

// Initialize global instance when DOM is ready
let animatedDemoVideo;

document.addEventListener('DOMContentLoaded', () => {
    animatedDemoVideo = new AnimatedDemoVideo('animatedDemoVideo');
});
