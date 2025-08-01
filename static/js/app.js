/*
===========================================================
    OnlyPans Recipe App - Main JavaScript
===========================================================
*/

// Initialize application when DOM is ready
document.addEventListener("DOMContentLoaded", function () {
    initializeApp();
});

function initializeApp() {
    initializeRatingSystem();
    initializeComments();
    initializeFormImagePreviews();
    initializeToasts();
    initializeModals();
    initializeDynamicForms();
    initializeTagSelection();
}

/**
 * Interactive Star Rating System
 */
function initializeRatingSystem() {
    const userRatingOverlay = document.querySelector(".user-rating-overlay");
    if (!userRatingOverlay) return;

    const stars = userRatingOverlay.querySelectorAll(".star-interactive");
    const ratingInput = document.getElementById("rating-value");
    const ratingForm = document.getElementById("rating-form");
    const currentRating =
        parseInt(userRatingOverlay.dataset.currentRating) || 0;

    // Set initial state
    updateStars(currentRating);

    stars.forEach((star, index) => {
        const rating = index + 1;

        // Hover effects
        star.addEventListener("mouseenter", function () {
            updateStars(rating, true);
        });

        star.addEventListener("mouseleave", function () {
            const selectedRating = parseInt(ratingInput.value) || currentRating;
            updateStars(selectedRating);
        });

        // Click to rate - auto submit
        star.addEventListener("click", function (e) {
            e.preventDefault();
            ratingInput.value = rating;
            updateStars(rating);

            // Show brief feedback
            const originalTitle = this.title;
            this.title = "Rating submitted!";
            setTimeout(() => {
                this.title = originalTitle;
            }, 2000);

            // Auto-submit immediately
            ratingForm.submit();
        });
    });

    function updateStars(rating, isHover = false) {
        stars.forEach((star, index) => {
            star.classList.remove("selected", "hover");
            if (index < rating) {
                star.classList.add(isHover ? "hover" : "selected");
            }
        });
    }
}

/**
 * Comment Reply System
 */
function initializeComments() {
    const replyBtns = document.querySelectorAll(".reply-btn");
    const cancelReplyBtns = document.querySelectorAll(".cancel-reply");

    replyBtns.forEach((btn) => {
        btn.addEventListener("click", function () {
            const commentId = this.dataset.commentId;
            const replyForm = document.getElementById(
                `reply-form-${commentId}`
            );

            // Hide all other reply forms
            document.querySelectorAll(".reply-form").forEach((form) => {
                form.style.display = "none";
            });

            // Show this reply form
            replyForm.style.display = "block";
            replyForm.querySelector("textarea").focus();
        });
    });

    cancelReplyBtns.forEach((btn) => {
        btn.addEventListener("click", function () {
            this.closest(".reply-form").style.display = "none";
        });
    });
}

/**
 * Image Preview for File Uploads
 */
function initializeFormImagePreviews() {
    // Profile image preview
    const profileImageInput = document.querySelector(
        'input[type="file"][name="profile_image"]'
    );
    if (profileImageInput) {
        profileImageInput.addEventListener("change", function (e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    const currentImg = document.querySelector(
                        'img[alt="Current profile picture"]'
                    );
                    if (currentImg) {
                        currentImg.src = e.target.result;
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Recipe image preview
    const recipeImageInput = document.querySelector(
        'input[type="file"][name="image"]'
    );
    if (recipeImageInput) {
        recipeImageInput.addEventListener("change", function (e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    // Create or update preview
                    let preview = document.querySelector(".image-preview");
                    if (!preview) {
                        preview = document.createElement("img");
                        preview.className =
                            "image-preview img-fluid rounded mt-2";
                        preview.style.maxHeight = "200px";
                        recipeImageInput.parentNode.appendChild(preview);
                    }
                    preview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }
}

/**
 * Toast Notifications
 */
function initializeToasts() {
    // Auto-show toasts
    const toastElements = document.querySelectorAll(".toast");
    toastElements.forEach((toastEl) => {
        const toast = new bootstrap.Toast(toastEl);
        toast.show();
    });
}

/**
 * Modal Functionality
 */
function initializeModals() {
    // Handle login/register modal switching
    const loginModal = document.getElementById("loginModal");
    const registerModal = document.getElementById("registerModal");

    if (loginModal && registerModal) {
        // Switch from login to register
        const switchToRegister = document.querySelector(
            '[data-bs-target="#registerModal"]'
        );
        if (switchToRegister) {
            switchToRegister.addEventListener("click", function () {
                const loginModalInstance =
                    bootstrap.Modal.getInstance(loginModal);
                if (loginModalInstance) {
                    loginModalInstance.hide();
                }
            });
        }

        // Switch from register to login
        const switchToLogin = document.querySelector(
            '[data-bs-target="#loginModal"]'
        );
        if (switchToLogin) {
            switchToLogin.addEventListener("click", function () {
                const registerModalInstance =
                    bootstrap.Modal.getInstance(registerModal);
                if (registerModalInstance) {
                    registerModalInstance.hide();
                }
            });
        }
    }
}

/**
 * Form Validation Helpers
 */
function showFieldError(fieldName, errorMessage) {
    const field = document.querySelector(`[name="${fieldName}"]`);
    if (field) {
        field.classList.add("is-invalid");

        // Create or update error feedback
        let errorDiv = field.parentNode.querySelector(".invalid-feedback");
        if (!errorDiv) {
            errorDiv = document.createElement("div");
            errorDiv.className = "invalid-feedback";
            field.parentNode.appendChild(errorDiv);
        }
        errorDiv.textContent = errorMessage;
    }
}

function clearFieldErrors() {
    document.querySelectorAll(".is-invalid").forEach((field) => {
        field.classList.remove("is-invalid");
    });
    document.querySelectorAll(".invalid-feedback").forEach((errorDiv) => {
        errorDiv.remove();
    });
}

/**
 * Dynamic Form Management
 */
function initializeDynamicForms() {
    // Add event listeners for remove buttons
    document.addEventListener("click", function (e) {
        if (e.target.matches(".btn-remove-row, .remove-row")) {
            removeRow(e.target);
        }
    });
}

function removeRow(button) {
    const row = button.closest(".ingredient-row, .step-row, .dynamic-form-row");
    if (row) {
        row.remove();
    }
}

function addIngredientRow() {
    const container = document.querySelector(".ingredient-container");
    if (!container) return;

    const lastRow = container.querySelector(".ingredient-row:last-child");
    if (lastRow) {
        const newRow = lastRow.cloneNode(true);

        // Clear input values
        newRow.querySelectorAll("input, select, textarea").forEach((input) => {
            if (input.type === "checkbox" || input.type === "radio") {
                input.checked = false;
            } else {
                input.value = "";
            }
        });

        // Update form indices if needed
        updateFormIndices(newRow, container.children.length);

        container.appendChild(newRow);
    }
}

function addStepRow() {
    const container = document.querySelector(".step-container");
    if (!container) return;

    const lastRow = container.querySelector(".step-row:last-child");
    if (lastRow) {
        const newRow = lastRow.cloneNode(true);

        // Clear input values
        newRow.querySelectorAll("input, select, textarea").forEach((input) => {
            if (input.type === "checkbox" || input.type === "radio") {
                input.checked = false;
            } else {
                input.value = "";
            }
        });

        // Update form indices if needed
        updateFormIndices(newRow, container.children.length);

        container.appendChild(newRow);
    }
}

function updateFormIndices(row, index) {
    // Update form field names and IDs to maintain proper Django formset structure
    row.querySelectorAll("input, select, textarea").forEach((field) => {
        if (field.name) {
            field.name = field.name.replace(/\d+/, index);
        }
        if (field.id) {
            field.id = field.id.replace(/\d+/, index);
        }
    });

    row.querySelectorAll("label").forEach((label) => {
        if (label.htmlFor) {
            label.htmlFor = label.htmlFor.replace(/\d+/, index);
        }
    });
}

/**
 * Utility Functions
 */
function showLoading(element) {
    element.classList.add("loading");
    element.disabled = true;
}

function hideLoading(element) {
    element.classList.remove("loading");
    element.disabled = false;
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export functions for use in other scripts
window.OnlyPansApp = {
    showFieldError,
    clearFieldErrors,
    showLoading,
    hideLoading,
    debounce,
    removeRow,
    addIngredientRow,
    addStepRow,
};

/**
 * Interactive Tag Selection for Forms
 */
function initializeTagSelection() {
    const tagSelections = document.querySelectorAll(".tag-selection");

    tagSelections.forEach((container) => {
        const selectableLabels = container.querySelectorAll(".tag-selectable");

        selectableLabels.forEach((label) => {
            label.addEventListener("click", function (e) {
                e.preventDefault();

                // Find the associated checkbox
                const checkbox = document.getElementById(
                    this.getAttribute("for")
                );
                if (checkbox) {
                    // Toggle the checkbox
                    checkbox.checked = !checkbox.checked;

                    // Update visual state
                    this.classList.toggle("tag-selected", checkbox.checked);

                    // Trigger change event for form validation
                    checkbox.dispatchEvent(
                        new Event("change", { bubbles: true })
                    );
                }
            });
        });

        // Initialize visual state based on existing checked checkboxes
        const checkboxes = container.querySelectorAll(".tag-checkbox");
        checkboxes.forEach((checkbox) => {
            const label = container.querySelector(
                `label[for="${checkbox.id}"]`
            );
            if (label && checkbox.checked) {
                label.classList.add("tag-selected");
            }
        });
    });
}
