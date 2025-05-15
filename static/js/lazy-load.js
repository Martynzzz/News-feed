document.addEventListener('DOMContentLoaded', () => {
  const imgs = document.querySelectorAll('.lazy-load');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.classList.remove('lazy-load');
          io.unobserve(img);
        }
      });
    });
    imgs.forEach(img => io.observe(img));
  } else {
    imgs.forEach(img => { img.src = img.dataset.src; });
  }
});
