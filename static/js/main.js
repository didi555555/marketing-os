document.addEventListener('DOMContentLoaded', function() {
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() { alert.style.display = 'none'; }, 5000);
    });

    var bars = document.querySelectorAll('.chart-bar');
    bars.forEach(function(bar) {
        bar.style.height = '0px';
        var target = bar.getAttribute('style').match(/height:\s*(\d+)px/);
        if (target) {
            setTimeout(function() {
                bar.style.height = target[1] + 'px';
            }, 200);
        }
    });

    var forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            var btn = form.querySelector('.btn-gold, .btn-primary, button[type="submit"]');
            if (btn) {
                btn.disabled = true;
                btn.textContent = 'جاري التحميل...';
            }
            var loadingEl = form.querySelector('.loading');
            if (loadingEl) loadingEl.classList.add('active');
        });
    });
});
