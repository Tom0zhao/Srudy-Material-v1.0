document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('back-to-top');
    const scrollThreshold = 200;
  
    // 显示/隐藏逻辑
    window.addEventListener('scroll', () => {
      btn.style.display = window.scrollY > scrollThreshold ? 'flex' : 'none';
    });
  
    // 点击事件
    btn.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  
    // 初始状态
    btn.style.display = 'none';
  });