// Random Thailand background rotator
(function () {
  const images = [
    "/static/images/thai-1.jpeg",
    "/static/images/thai-2.jpeg",
    "/static/images/thai-3.webp",
    "/static/images/thai-4.jpeg",
  ];

  const pick = images[Math.floor(Math.random() * images.length)];

  const style = document.createElement("style");
  style.innerHTML = `
    body::before {
      content: "";
      position: fixed;
      inset: 0;
      background:
        linear-gradient(to bottom, rgba(2,14,20,0.45), rgba(2,14,20,0.45)),
        url("${pick}") center / cover no-repeat fixed;
      z-index: -1;
    }
  `;
  document.head.appendChild(style);
})();

