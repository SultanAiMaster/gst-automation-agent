// Interactive Demo Controller
class InteractiveDemo {
    constructor() {
        this.currentStep = 0;
        this.totalSteps = 5;
        this.demoData = {
            invoiceNumber: 'INV-2026-DEMO',
            customerName: '',
            amount: 0,
            gstRate: 18
        };
        this.init();
    }

    init() {
        this.renderDemo();
        this.startDemo();
    }

    renderDemo() {
        const demoContainer = document.getElementById('interactiveDemo');
        if (!demoContainer) return;

        demoContainer.innerHTML = `
            <div class="demo-interactive">
                <div class="floating-icon" style="top: 10%; left: 5%;">📄</div>
                <div class="floating-icon" style="top: 60%; right: 5%;">💰</div>
                <div class="floating-icon" style="bottom: 10%; left: 15%;">✅</div>

                <div class="demo-progress-bar">
                    <div class="demo-progress-fill" id="progressFill"></div>
                </div>

                <div id="stepContainer"></div>
            </div>
        `;
    }

    startDemo() {
        this.showStep(0);
    }

    showStep(step) {
        const container = document.getElementById('stepContainer');
        this.currentStep = step;
        this.updateProgress();

        const steps = [
            this.getStep1(),
            this.getStep2(),
            this.getStep3(),
            this.getStep4(),
            this.getStep5()
        ];

        container.innerHTML = steps[step];
        this.addStepListeners(step);
    }

    getStep1() {
        return `
            <div class="demo-step active" id="step1">
                <div class="demo-step-title">📝 Step 1: Enter Invoice Details</div>
                <div class="demo-step-content">
                    <p>Enter your invoice details below:</p>
                    <input type="text" class="demo-input" id="demoInvoiceNumber" placeholder="Invoice Number" value="${this.demoData.invoiceNumber}">
                    <input type="text" class="demo-input" id="demoCustomerName" placeholder="Customer Name">
                    <input type="number" class="demo-input" id="demoAmount" placeholder="Amount (₹)">
                    <button class="demo-btn" onclick="demo.nextStep(1)">
                        <i class="fas fa-arrow-right"></i> Continue
                    </button>
                </div>
            </div>
        `;
    }

    getStep2() {
        return `
            <div class="demo-step active" id="step2">
                <div class="demo-step-title">🔍 Step 2: GSTIN Validation</div>
                <div class="demo-step-content">
                    <p>Enter customer GSTIN for validation:</p>
                    <input type="text" class="demo-input" id="demoGSTIN" placeholder="GSTIN (e.g., 27ABCDE1234F1Z5)">
                    <div class="demo-btn" style="background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2);">
                        <i class="fas fa-check-circle" style="color: #00b894;"></i>
                        <span>Auto-validating in background...</span>
                    </div>
                    <button class="demo-btn" onclick="demo.nextStep(2)">
                        <i class="fas fa-check"></i> Validation Complete
                    </button>
                </div>
            </div>
        `;
    }

    getStep3() {
        return `
            <div class="demo-step active" id="step3">
                <div class="demo-step-title">⚡ Step 3: Auto GST Calculation</div>
                <div class="demo-step-content">
                    <p>GST calculated automatically!</p>
                    <div class="demo-result">
                        <h4>Taxable Amount</h4>
                        <div class="amount">₹${this.demoData.amount || '10,000'}</div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;">
                            <div>
                                <h4 style="color: #00f2fe;">CGST (9%)</h4>
                                <div style="font-size: 1.5rem; font-weight: 600;">₹${(this.demoData.amount * 0.09 || 900).toLocaleString()}</div>
                            </div>
                            <div>
                                <h4 style="color: #00f2fe;">SGST (9%)</h4>
                                <div style="font-size: 1.5rem; font-weight: 600;">₹${(this.demoData.amount * 0.09 || 900).toLocaleString()}</div>
                            </div>
                        </div>
                    </div>
                    <button class="demo-btn" onclick="demo.nextStep(3)">
                        <i class="fas fa-arrow-right"></i> Next
                    </button>
                </div>
            </div>
        `;
    }

    getStep4() {
        return `
            <div class="demo-step active" id="step4">
                <div class="demo-step-title">📄 Step 4: PDF Invoice Generation</div>
                <div class="demo-step-content">
                    <p>Generating professional GST-compliant invoice...</p>
                    <div class="demo-btn" style="background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2);">
                        <i class="fas fa-cog fa-spin" style="color: #00f2fe;"></i>
                        <span>Creating PDF with ReportLab...</span>
                    </div>
                    <div style="background: rgba(0, 184, 148, 0.1); border: 1px solid #00b894; border-radius: 10px; padding: 20px; margin-top: 20px;">
                        <div class="success-check"><i class="fas fa-check"></i></div>
                        <h4 style="color: #00b894; margin: 10px 0;">PDF Generated Successfully!</h4>
                        <p style="font-size: 0.9rem; color: rgba(255,255,255,0.7);">
                            Invoice number: ${this.demoData.invoiceNumber}<br>
                            File: invoice_${this.demoData.invoiceNumber.replace(/\//g, '-')}.pdf
                        </p>
                    </div>
                    <button class="demo-btn" onclick="demo.nextStep(4)">
                        <i class="fas fa-download"></i> Download PDF
                    </button>
                </div>
            </div>
        `;
    }

    getStep5() {
        return `
            <div class="demo-step active" id="step5">
                <div class="demo-step-title">🎉 Step 5: Ready to File GSTR</div>
                <div class="demo-step-content" style="text-align: center;">
                    <p style="font-size: 1.2rem; margin-bottom: 30px;">
                        Your invoice is ready! GST returns data updated automatically.
                    </p>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px;">
                        <div style="background: rgba(0, 184, 148, 0.1); padding: 20px; border-radius: 10px; border: 1px solid #00b894;">
                            <i class="fas fa-file-alt" style="font-size: 2rem; color: #00b894; margin-bottom: 10px;"></i>
                            <h5>GSTR-1</h5>
                            <p style="font-size: 0.8rem; color: rgba(255,255,255,0.6);">Updated</p>
                        </div>
                        <div style="background: rgba(0, 184, 148, 0.1); padding: 20px; border-radius: 10px; border: 1px solid #00b894;">
                            <i class="fas fa-file-alt" style="font-size: 2rem; color: #00b894; margin-bottom: 10px;"></i>
                            <h5>GSTR-3B</h5>
                            <p style="font-size: 0.8rem; color: rgba(255,255,255,0.6);">Ready to file</p>
                        </div>
                        <div style="background: rgba(0, 242, 254, 0.1); padding: 20px; border-radius: 10px; border: 1px solid #00f2fe;">
                            <i class="fas fa-bell" style="font-size: 2rem; color: #00f2fe; margin-bottom: 10px;"></i>
                            <h5>Reminder</h5>
                            <p style="font-size: 0.8rem; color: rgba(255,255,255,0.6);">20th of this month</p>
                        </div>
                    </div>
                    <div style="background: linear-gradient(135deg, #00b894, #00f2fe); padding: 30px; border-radius: 15px; margin-bottom: 20px;">
                        <h3 style="font-size: 2rem; margin-bottom: 10px;">Time Saved: 90% 🚀</h3>
                        <p style="font-size: 1rem; opacity: 0.9;">
                            Manual process: 30 minutes | Bharat GST AI: 3 minutes
                        </p>
                    </div>
                    <button class="demo-btn" onclick="demo.restartDemo()">
                        <i class="fas fa-redo"></i> Start New Demo
                    </button>
                </div>
            </div>
        `;
    }

    addStepListeners(step) {
        if (step === 0) {
            const amountInput = document.getElementById('demoAmount');
            if (amountInput) {
                amountInput.addEventListener('input', (e) => {
                    this.demoData.amount = parseFloat(e.target.value) || 0;
                });
            }
        }
    }

    nextStep(currentStep) {
        // Validate and save data
        if (currentStep === 0) {
            const customerName = document.getElementById('demoCustomerName').value;
            const amount = document.getElementById('demoAmount').value;
            if (!customerName || !amount) {
                alert('Please fill in all fields');
                return;
            }
            this.demoData.customerName = customerName;
            this.demoData.amount = parseFloat(amount);
        }

        // Mark current step as completed
        const currentStepEl = document.getElementById(`step${currentStep + 1}`);
        if (currentStepEl) {
            currentStepEl.classList.add('completed');
        }

        // Move to next step after delay
        setTimeout(() => {
            this.showStep(currentStep + 1);
        }, 500);
    }

    updateProgress() {
        const progress = ((this.currentStep + 1) / this.totalSteps) * 100;
        const progressFill = document.getElementById('progressFill');
        if (progressFill) {
            progressFill.style.width = `${progress}%`;
        }
    }

    restartDemo() {
        this.currentStep = 0;
        this.demoData = {
            invoiceNumber: 'INV-2026-DEMO',
            customerName: '',
            amount: 0,
            gstRate: 18
        };
        this.showStep(0);
    }
}

// Initialize demo when page loads
let demo;
document.addEventListener('DOMContentLoaded', () => {
    demo = new InteractiveDemo();
});
