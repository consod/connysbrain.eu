document.addEventListener('DOMContentLoaded', function () {
  const gallery = document.getElementById('lightgallery');
  if (gallery && typeof lightGallery !== 'undefined') {
    lightGallery(gallery, {
      selector: 'a', // Explicitly target only anchor tags
      thumbnail: true,
      animateThumb: false,
      showThumbByDefault: false,
      download: true
    });
  }
});
