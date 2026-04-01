(() => {
  const textarea = document.getElementById("review-input");
  const counter = document.getElementById("char-count");
  const form = document.getElementById("review-form");
  const submitBtn = document.getElementById("submit-btn");
  const submitStatus = document.getElementById("submit-status");
  const batchForm = document.getElementById("batch-form");
  const batchFileInput = document.getElementById("batch-file");
  const batchFileName = document.getElementById("batch-file-name");
  const batchSubmitBtn = document.getElementById("batch-submit-btn");
  const batchSubmitStatus = document.getElementById("batch-submit-status");

  if (textarea && counter) {
    const max = parseInt(textarea.getAttribute("maxlength") || "0", 10);
    const updateCounter = () => {
      const length = textarea.value.length;
      counter.textContent = `${length} / ${max}`;
      counter.classList.toggle("text-rose-300", length > max * 0.9);
      counter.classList.toggle("text-emerald-300", length <= max * 0.9);
    };

    updateCounter();
    textarea.addEventListener("input", updateCounter);
  }

  if (form && submitBtn) {
    form.addEventListener("submit", () => {
      submitBtn.classList.add("is-loading");
      submitBtn.setAttribute("disabled", "disabled");
      if (submitStatus) {
        submitStatus.textContent = "Analyzing sentiment...";
      }
    });
  }

  if (batchFileInput && batchFileName) {
    batchFileInput.addEventListener("change", () => {
      const [file] = batchFileInput.files || [];
      batchFileName.textContent = file ? file.name : "No file selected";
    });
  }

  if (batchForm && batchSubmitBtn) {
    batchForm.addEventListener("submit", () => {
      batchSubmitBtn.classList.add("is-loading");
      batchSubmitBtn.setAttribute("disabled", "disabled");
      if (batchSubmitStatus) {
        batchSubmitStatus.textContent = "Validating CSV upload...";
      }
    });
  }
})();
