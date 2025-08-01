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
    initializeRecipeControls();
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
    // Only auto-show toasts that have content (Django messages)
    const messageToasts = document.querySelectorAll(".toast:not(#authToast):not(#recipeSuccessToast)");
    messageToasts.forEach((toastEl) => {
        // Check if toast has actual content
        const toastBody = toastEl.querySelector('.toast-body');
        if (toastBody && toastBody.textContent.trim()) {
            const toast = new bootstrap.Toast(toastEl, {
                autohide: true,
                delay: 4000,
            });
            toast.show();
        }
    });

    // Check for success messages and show in recipe success toast instead
    const successMessages = document.querySelectorAll('.toast.bg-custom-success .toast-body');
    successMessages.forEach((messageBody) => {
        if (messageBody.textContent.trim()) {
            showRecipeSuccessToast(messageBody.textContent.trim());
            // Hide the original success toast
            const originalToast = messageBody.closest('.toast');
            if (originalToast) {
                originalToast.style.display = 'none';
            }
        }
    });
}

/**
 * Show Recipe Success Toast
 */
function showRecipeSuccessToast(message) {
    const toastElement = document.getElementById("recipeSuccessToast");
    const toastMessage = document.getElementById("recipeSuccessToastMessage");

    if (toastElement && toastMessage) {
        toastMessage.textContent = message;

        const toast = new bootstrap.Toast(toastElement, {
            autohide: true,
            delay: 5000,
        });
        toast.show();
    }
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
    showRecipeSuccessToast,
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

/**
 * Recipe Controls - Servings Scaler and Unit Converter
 */
function initializeRecipeControls() {
    // Servings scaler elements
    const servingsInputs = document.querySelectorAll(
        "#servings-scaler, #servings-scaler-mobile"
    );
    const decreaseButtons = document.querySelectorAll(
        "#decrease-servings, #decrease-servings-mobile"
    );
    const increaseButtons = document.querySelectorAll(
        "#increase-servings, #increase-servings-mobile"
    );

    // Unit system toggles
    const unitToggles = document.querySelectorAll(
        "#unit-system-toggle, #unit-system-toggle-mobile"
    );
    const unitLabels = document.querySelectorAll(
        "#unit-system-label, #unit-system-label-mobile"
    );

    // Get original serving size
    const originalServings = parseInt(servingsInputs[0]?.dataset.original) || 1;
    let isAmericanUnits = false;

    // Servings scaler functionality
    servingsInputs.forEach((input) => {
        input.addEventListener("change", updateIngredientQuantities);
        input.addEventListener("input", updateIngredientQuantities);
    });

    decreaseButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
            servingsInputs.forEach((input) => {
                const current = parseInt(input.value);
                if (current > 1) {
                    input.value = current - 1;
                    updateIngredientQuantities();
                }
            });
        });
    });

    increaseButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
            servingsInputs.forEach((input) => {
                const current = parseInt(input.value);
                if (current < 20) {
                    input.value = current + 1;
                    updateIngredientQuantities();
                }
            });
        });
    });

    // Unit system toggle functionality
    unitToggles.forEach((toggle) => {
        toggle.addEventListener("change", (e) => {
            isAmericanUnits = e.target.checked;

            // Sync all toggles
            unitToggles.forEach((otherToggle) => {
                otherToggle.checked = isAmericanUnits;
            });

            // Update labels
            unitLabels.forEach((label) => {
                label.textContent = isAmericanUnits ? "US" : "Metric";
            });

            updateIngredientQuantities();
        });
    });

    function updateIngredientQuantities() {
        const currentServings =
            parseInt(servingsInputs[0]?.value) || originalServings;
        const scaleFactor = currentServings / originalServings;

        document.querySelectorAll(".ingredient-amount").forEach((element) => {
            const originalQuantity = parseFloat(
                element.dataset.originalQuantity
            );
            const unit = element.dataset.unit;
            const unitName = element.dataset.unitName;

            // Check if this is a "to taste" or similar non-scalable unit
            const nonScalableUnits = [
                'to taste', 'taste', 'pinch', 'dash', 'handful', 
                'splash', 'drizzle', 'sprinkle', 'garnish'
            ];
            
            const isNonScalable = nonScalableUnits.some(nonScalableUnit => 
                unitName.toLowerCase().includes(nonScalableUnit.toLowerCase())
            );

            if (isNonScalable) {
                // Don't scale "to taste" type measurements, and show without quantity
                element.textContent = unitName; // Just show the unit name
                return;
            }

            if (isAmericanUnits) {
                // Convert to American units
                const convertedAmount = getAmericanConversion(
                    originalQuantity,
                    unitName,
                    scaleFactor
                );
                element.textContent = convertedAmount;
            } else {
                // Use metric with scaling
                const scaledQuantity = originalQuantity * scaleFactor;
                const formattedQuantity =
                    scaledQuantity % 1 === 0
                        ? scaledQuantity.toString()
                        : scaledQuantity.toFixed(1).replace(/\.?0+$/, "");
                element.textContent = `${formattedQuantity} ${unit}`;
            }
        });
    }

    function getAmericanConversion(quantity, unitName, scale) {
        const unit = unitName.toLowerCase();
        
        // Check if this is a non-scalable unit
        const nonScalableUnits = [
            'to taste', 'taste', 'pinch', 'dash', 'handful', 
            'splash', 'drizzle', 'sprinkle', 'garnish'
        ];
        
        const isNonScalable = nonScalableUnits.some(nonScalableUnit => 
            unit.includes(nonScalableUnit.toLowerCase())
        );

        if (isNonScalable) {
            // Don't scale "to taste" type measurements, just show unit name
            return unitName; // Keep original casing
        }

        const scaledQuantity = quantity * scale;

        // Volume conversions
        if (unit.includes("ml") || unit.includes("milliliter")) {
            if (scaledQuantity >= 1000) {
                const cups = scaledQuantity / 240;
                return `${cups.toFixed(1)} Cup${cups > 1 ? "s" : ""}`;
            } else if (scaledQuantity >= 250) {
                return `${(scaledQuantity / 240).toFixed(1)} Cups`;
            } else if (scaledQuantity >= 15) {
                return `${(scaledQuantity / 15).toFixed(1)} Tbsp`;
            } else {
                return `${(scaledQuantity / 5).toFixed(1)} Tsp`;
            }
        }

        // Weight conversions
        if (unit.includes("gram") || unit === "g") {
            if (scaledQuantity >= 450) {
                return `${(scaledQuantity / 453.6).toFixed(1)} Lb${
                    scaledQuantity > 900 ? "s" : ""
                }`;
            } else if (scaledQuantity >= 28) {
                return `${(scaledQuantity / 28.35).toFixed(1)} Oz`;
            }
        }

        if (unit.includes("kilogram") || unit === "kg") {
            return `${(scaledQuantity * 2.2).toFixed(1)} Lbs`;
        }

        // Liter conversions
        if (unit.includes("liter") || unit === "l") {
            return `${(scaledQuantity * 4.2).toFixed(1)} Cups`;
        }

        // Default: return scaled original with proper casing
        const formattedQuantity =
            scaledQuantity % 1 === 0
                ? scaledQuantity.toString()
                : scaledQuantity.toFixed(1).replace(/\.?0+$/, "");
        return `${formattedQuantity} ${unitName}`; // Keep original casing
    }
}
