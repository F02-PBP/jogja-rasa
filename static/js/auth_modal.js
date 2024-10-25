window.showLoginModal = function (event) {
  if (event) {
    event.preventDefault();
  }
  const modal = document.getElementById("pleaseLoginModal");
  if (!modal) return;

  modal.classList.remove("hidden");
  const modalContent = modal.querySelector("div");

  setTimeout(() => {
    modalContent.classList.remove("scale-95");
    modalContent.classList.add("scale-100");
  }, 10);
};

window.hideLoginModal = function () {
  const modal = document.getElementById("pleaseLoginModal");
  if (!modal) return;

  const modalContent = modal.querySelector("div");
  modalContent.classList.remove("scale-100");
  modalContent.classList.add("scale-95");

  setTimeout(() => {
    modal.classList.add("hidden");
  }, 300);
};

function initializeModal() {
  const modal = document.getElementById("pleaseLoginModal");
  if (!modal) return;

  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      hideLoginModal();
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      hideLoginModal();
    }
  });
}

function initializeAuthLinks() {
  const authLinks = document.querySelectorAll(".auth-required");
  authLinks.forEach((link) => {
    link.addEventListener("click", showLoginModal);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initializeModal();
  initializeAuthLinks();
});
