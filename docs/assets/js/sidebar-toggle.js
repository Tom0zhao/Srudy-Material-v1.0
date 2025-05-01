document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.querySelector('.sidebar');
    const content = document.querySelector('.content');
    const toggleBtn = document.getElementById('sidebar-toggle');
  
    // 初始化状态
    const storedState = localStorage.getItem('sidebarCollapsed');
    const isCollapsed = storedState ? JSON.parse(storedState) : false;
  
    // 设置初始状态
    sidebar.style.transform = isCollapsed ? 'translateX(-100%)' : '';
    content.style.marginLeft = isCollapsed ? '20px' : '260px';
  
    // 点击事件处理
    toggleBtn.addEventListener('click', () => {
      const isCollapsed = sidebar.style.transform === 'translateX(-100%)';
      
      if (isCollapsed) {
        sidebar.style.transform = '';
        content.style.marginLeft = '260px';
      } else {
        sidebar.style.transform = 'translateX(-100%)';
        content.style.marginLeft = '20px';
      }
      
      localStorage.setItem('sidebarCollapsed', !isCollapsed);
    });
  
    // 窗口调整时自动处理
    window.addEventListener('resize', () => {
      if (window.innerWidth <= 768) {
        sidebar.style.transform = 'translateX(-100%)';
        content.style.marginLeft = '20px';
      } else {
        const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
        sidebar.style.transform = isCollapsed ? 'translateX(-100%)' : '';
        content.style.marginLeft = isCollapsed ? '20px' : '260px';
      }
    });
  });