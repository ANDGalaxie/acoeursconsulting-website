const navToggle = document.querySelector("[data-nav-toggle]");
const navPanel = document.querySelector("[data-nav-panel]");
const siteHeader = document.querySelector("[data-site-header]");
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

if (siteHeader) {
    const syncHeaderState = () => {
        siteHeader.classList.toggle("is-scrolled", window.scrollY > 8);
    };

    syncHeaderState();
    window.addEventListener("scroll", syncHeaderState, { passive: true });
}

if (navToggle && navPanel) {
    const navLinks = Array.from(navPanel.querySelectorAll("a"));
    const getFocusableItems = () => [navToggle, ...navLinks];

    const syncNavigationState = (isOpen) => {
        navToggle.setAttribute("aria-expanded", String(isOpen));
        navToggle.setAttribute("aria-label", isOpen ? "关闭主导航菜单" : "打开主导航菜单");
        navPanel.classList.toggle("is-open", isOpen);
        navPanel.setAttribute("aria-hidden", String(!isOpen));

        if (window.innerWidth < 768) {
            if (isOpen) {
                navLinks[0]?.focus();
            } else {
                navToggle.focus();
            }
        }
    };

    syncNavigationState(false);

    navToggle.addEventListener("click", () => {
        const isOpen = navToggle.getAttribute("aria-expanded") === "true";
        syncNavigationState(!isOpen);
    });

    navLinks.forEach((link) => {
        link.addEventListener("click", () => {
            if (window.innerWidth < 768) {
                syncNavigationState(false);
            }
        });
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            syncNavigationState(false);
        }

        if (
            event.key === "Tab" &&
            window.innerWidth < 768 &&
            navToggle.getAttribute("aria-expanded") === "true"
        ) {
            const focusableItems = getFocusableItems();
            const firstItem = focusableItems[0];
            const lastItem = focusableItems[focusableItems.length - 1];

            if (event.shiftKey && document.activeElement === firstItem) {
                event.preventDefault();
                lastItem?.focus();
            } else if (!event.shiftKey && document.activeElement === lastItem) {
                event.preventDefault();
                firstItem?.focus();
            }
        }
    });

    window.addEventListener("resize", () => {
        if (window.innerWidth >= 768) {
            navPanel.removeAttribute("aria-hidden");
            navPanel.classList.remove("is-open");
            navToggle.setAttribute("aria-expanded", "false");
            navToggle.setAttribute("aria-label", "打开主导航菜单");
            return;
        }

        syncNavigationState(false);
    });
}

const setupRevealAnimations = () => {
    if (prefersReducedMotion.matches) {
        return;
    }

    const revealGroups = [
        { selector: ".about-section__copy", reveal: "soft" },
        { selector: ".about-section__visual", reveal: "right", delayStep: 80 },
        { selector: ".about-capability", delayStep: 80 },
        { selector: ".stage-section .section-heading", reveal: "soft" },
        { selector: ".stage-card", delayStep: 90 },
        { selector: ".service-feature", reveal: "soft" },
        { selector: ".service-item", delayStep: 80 },
        { selector: ".home-section--personal .section-heading", reveal: "soft" },
        { selector: ".personal-item", delayStep: 80 },
        { selector: ".process-section .section-heading", reveal: "soft" },
        { selector: ".process-stage", delayStep: 80 },
        { selector: ".process-section .section-actions", delayStep: 240, reveal: "soft" },
        { selector: ".case-study__intro", reveal: "soft" },
        { selector: ".case-study__visual", reveal: "left", delayStep: 40 },
        { selector: ".case-overview__content", reveal: "right", delayStep: 120 },
        { selector: ".case-study__section", delayStep: 90 },
        { selector: ".case-study__results li", delayStep: 90 },
        { selector: ".case-study__footer", delayStep: 140, reveal: "soft" },
        { selector: ".why-section__heading", reveal: "soft" },
        { selector: ".why-stats", delayStep: 80, reveal: "soft" },
        { selector: ".advantage-row", delayStep: 70 },
        { selector: ".why-section__closing", delayStep: 120, reveal: "soft" },
        { selector: ".final-cta", reveal: "soft" },
        { selector: ".site-footer__inner", reveal: "soft" },
    ];

    const revealElements = [];

    revealGroups.forEach(({ selector, delayStep = 0, reveal = "up" }) => {
        const elements = document.querySelectorAll(selector);

        elements.forEach((element, index) => {
            element.classList.add("reveal-on-scroll");
            if (reveal !== "up") {
                element.dataset.reveal = reveal;
            }
            if (delayStep > 0) {
                element.style.setProperty("--reveal-delay", `${index * delayStep}ms`);
            }
            revealElements.push(element);
        });
    });

    if (!revealElements.length) {
        return;
    }

    document.body.classList.add("has-motion");

    if (!("IntersectionObserver" in window)) {
        revealElements.forEach((element) => {
            element.classList.add("is-visible");
        });
        return;
    }

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) {
                    return;
                }

                entry.target.classList.add("is-visible");
                observer.unobserve(entry.target);
            });
        },
        {
            threshold: 0.16,
            rootMargin: "0px 0px -12% 0px",
        },
    );

    revealElements.forEach((element) => {
        observer.observe(element);
    });
};

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setupRevealAnimations, { once: true });
} else {
    setupRevealAnimations();
}
