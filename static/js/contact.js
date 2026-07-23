document.documentElement.classList.add("has-js");

const contactForm = document.querySelector("[data-contact-form]");

if (contactForm) {
    const stepPanels = Array.from(contactForm.querySelectorAll("[data-step-panel]"));
    const stepTitles = stepPanels.map((panel) => panel.querySelector("[data-step-title]"));
    const identityInputs = Array.from(contactForm.querySelectorAll('input[name="identity"]'));
    const directionGroups = Array.from(contactForm.querySelectorAll("[data-direction-group]"));
    const companyField = contactForm.querySelector("[data-company-field]");
    const progressItems = Array.from(document.querySelectorAll(".contact-progress__item"));
    const mobileStep = document.querySelector(".contact-progress-mobile__step");
    const mobileLabel = document.querySelector(".contact-progress-mobile__label");
    const mobileBar = document.querySelector(".contact-progress-mobile__bar");
    const optionalToggle = contactForm.querySelector("[data-contact-optional-toggle]");
    const optionalDetails = contactForm.querySelector("[data-contact-optional-details]");
    let currentStep = Number(contactForm.closest("[data-current-step]")?.dataset.currentStep || 1);

    const stepLabels = {
        1: "关于您",
        2: "您的需求",
        3: "联系方式",
    };

    const getCheckedIdentity = () => {
        const checked = identityInputs.find((input) => input.checked);
        return checked ? checked.value : "";
    };

    const syncCompanyField = () => {
        if (!companyField) {
            return;
        }

        const identity = getCheckedIdentity();
        const shouldShow = identity === "company" || identity === "owner_investor";
        companyField.hidden = !shouldShow;
    };

    const syncDirectionGroups = () => {
        const identity = getCheckedIdentity();
        let selectedInput = contactForm.querySelector('input[name="consultation_direction"]:checked');

        directionGroups.forEach((group) => {
            const identities = (group.dataset.identities || "").split(/\s+/).filter(Boolean);
            const shouldShow = !identity || identities.includes(identity);
            const inputs = Array.from(group.querySelectorAll('input[name="consultation_direction"]'));

            group.hidden = !shouldShow;
            inputs.forEach((input) => {
                input.disabled = !shouldShow;
            });
        });

        if (selectedInput) {
            const selectedGroup = selectedInput.closest("[data-direction-group]");
            if (selectedGroup?.hidden) {
                selectedInput.checked = false;
                selectedInput = null;
            }
        }
    };

    const syncOptionalDetails = (expanded) => {
        if (!optionalToggle || !optionalDetails) {
            return;
        }

        optionalToggle.setAttribute("aria-expanded", expanded ? "true" : "false");
        optionalToggle.textContent = expanded ? "收起补充信息" : "＋ 补充咨询信息（选填）";
        optionalDetails.hidden = !expanded;
    };

    const updateProgress = (step) => {
        progressItems.forEach((item, index) => {
            const itemStep = index + 1;
            item.classList.toggle("is-current", itemStep === step);
            item.classList.toggle("is-complete", itemStep < step);
            if (itemStep === step) {
                item.setAttribute("aria-current", "step");
            } else {
                item.removeAttribute("aria-current");
            }
        });

        if (mobileStep) {
            mobileStep.textContent = `第 ${step} 步，共 3 步`;
        }
        if (mobileLabel) {
            mobileLabel.textContent = stepLabels[step];
        }
        if (mobileBar) {
            mobileBar.className = `contact-progress-mobile__bar contact-progress-mobile__bar--step-${step}`;
        }
    };

    const showStep = (step, shouldFocus = true) => {
        currentStep = step;
        stepPanels.forEach((panel) => {
            const isCurrent = Number(panel.dataset.stepPanel) === step;
            panel.hidden = !isCurrent;
            panel.classList.toggle("is-entering", isCurrent);
        });
        updateProgress(step);
        syncCompanyField();
        syncDirectionGroups();

        if (shouldFocus) {
            requestAnimationFrame(() => {
                stepTitles[step - 1]?.focus();
            });
        }

        setTimeout(() => {
            stepPanels.forEach((panel) => panel.classList.remove("is-entering"));
        }, 260);
    };

    const validateContactStep = (step) => {
        if (step === 1) {
            const checked = getCheckedIdentity();
            if (!checked) {
                identityInputs[0]?.reportValidity();
                return false;
            }
            return true;
        }

        if (step === 2) {
            const directionInputs = Array.from(contactForm.querySelectorAll('input[name="consultation_direction"]'));
            const checked = directionInputs.find((input) => input.checked);

            if (!checked) {
                directionInputs[0]?.reportValidity();
                return false;
            }
            return true;
        }

        if (step === 3) {
            const name = contactForm.querySelector("#id_name");
            const email = contactForm.querySelector("#id_email");
            const phone = contactForm.querySelector("#id_phone");
            const consent = contactForm.querySelector("#id_privacy_consent");

            if (name && !name.reportValidity()) {
                return false;
            }

            if (email && email.value && !email.reportValidity()) {
                return false;
            }

            if (phone && email && !phone.value.trim() && !email.value.trim()) {
                const message = "请至少填写联系电话或电子邮箱中的一项。";
                phone.setCustomValidity(message);
                email.setCustomValidity(message);
                const valid = phone.reportValidity();
                phone.setCustomValidity("");
                email.setCustomValidity("");
                return valid;
            }

            if (consent && !consent.reportValidity()) {
                return false;
            }
        }

        return true;
    };

    identityInputs.forEach((input) => {
        input.addEventListener("change", () => {
            syncCompanyField();
            syncDirectionGroups();
        });
    });

    contactForm.querySelectorAll("[data-step-next]").forEach((button) => {
        button.addEventListener("click", () => {
            if (!validateContactStep(currentStep)) {
                return;
            }
            showStep(Number(button.dataset.stepNext));
        });
    });

    contactForm.querySelectorAll("[data-step-prev]").forEach((button) => {
        button.addEventListener("click", () => {
            showStep(Number(button.dataset.stepPrev));
        });
    });

    contactForm.addEventListener("submit", (event) => {
        if (!validateContactStep(3)) {
            event.preventDefault();
            showStep(3, false);
        }
    });

    if (optionalToggle && optionalDetails) {
        optionalToggle.addEventListener("click", () => {
            syncOptionalDetails(optionalDetails.hidden);
        });
    }

    syncCompanyField();
    syncDirectionGroups();
    if (optionalToggle && optionalDetails) {
        syncOptionalDetails(optionalToggle.getAttribute("aria-expanded") === "true");
    }
    showStep(currentStep, false);
}
