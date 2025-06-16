function toggleSidebar() {
         const sidebar = document.getElementById("sidebar");
         const toggleBtn = document.getElementById("toggleBtn");
         const toggleBlock = document.getElementById("toggleBlock");
         const content = document.getElementById("content");
         const isMobile = window.innerWidth <= 768;

         sidebar.classList.toggle("active");
         if (isMobile) {
            toggleBtn.classList.toggle("hidden");
            toggleBlock.classList.toggle("active");
            content.classList.toggle("active");
         }
      }

      // blur effect a
      window.addEventListener('resize', () => {
         const sidebar = document.getElementById("sidebar");
         const toggleBtn = document.getElementById("toggleBtn");
         const toggleBlock = document.getElementById("toggleBlock");
         const content = document.getElementById("content");
         const isMobile = window.innerWidth <= 768;

         if (!isMobile && sidebar.classList.contains("active")) {
            sidebar.classList.remove("active");
            toggleBtn.classList.remove("hidden");
            toggleBlock.classList.remove("active");
            content.classList.remove("active");
         }
      });