const gallery = document.getElementById("lightgallery");
if (gallery && typeof lightGallery !== "undefined") {
  lightGallery(gallery, {
    selector: "a",
    thumbnail: true,
    animateThumb: false,
    showThumbByDefault: false,
    download: true,
    // Enable lazy loading
    lazy: true,
    // Only load next/previous images
    preload: 1,
  });
}
