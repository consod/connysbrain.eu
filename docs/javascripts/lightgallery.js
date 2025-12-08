// Wait for Zensical's JavaScript runtime to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
  // Check if lightGallery is available and the gallery container exists
  const gallery = document.getElementById('lightgallery');
  if (gallery && typeof lightGallery !== 'undefined') {
    // Initialize lightGallery with proper options
    lightGallery(gallery, {
      selector: 'a',
      thumbnail: true,
      animateThumb: false,
      showThumbByDefault: false,
      download: false
    });
  }
});
