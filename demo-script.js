    <script>
        function playDemo() {
            const video = document.getElementById('demoVideo');
            const placeholder = document.getElementById('demoPlaceholder');
            const overlay = document.querySelector('.demo-overlay');

            placeholder.style.display = 'none';
            overlay.style.display = 'none';
            video.style.display = 'block';
            video.src += '&autoplay=1';
        }

        // Intersection Observer for scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        document.querySelectorAll('.slide-up').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(50px)';
            el.style.transition = 'all 0.6s ease';
            observer.observe(el);
        });
    </script>
