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
        { selector: ".about-section__copy", reveal: "title" },
        { selector: ".about-section__visual", reveal: "image-right", delay: 150 },
        { selector: ".about-capability", reveal: "item", delayStep: 100, maxDelay: 330 },
        { selector: ".stage-section .section-heading", reveal: "title" },
        { selector: ".stage-card", reveal: "item", delayStep: 100, maxDelay: 300 },
        { selector: ".service-feature", reveal: "panel" },
        {
            selector: ".service-item",
            reveal: "item",
            delay(index) {
                return Math.floor(index / 2) * 130 + (index % 2) * 40;
            },
            maxDelay: 170,
        },
        { selector: ".home-section--personal .section-heading", reveal: "title" },
        { selector: ".personal-panel", reveal: "panel", delay: 70 },
        { selector: ".personal-item", reveal: "item", delayStep: 90, maxDelay: 180 },
        { selector: ".process-section .section-heading", reveal: "title" },
        { selector: ".process-timeline", reveal: "panel", delay: 80 },
        { selector: ".process-stage", reveal: "item", delayStep: 100, maxDelay: 440 },
        { selector: ".process-section .section-actions", delay: 520, reveal: "button" },
        { selector: ".case-study__intro", reveal: "title" },
        { selector: ".case-study__visual", reveal: "image-left", delay: 120 },
        { selector: ".case-overview__content", reveal: "panel", delay: 230 },
        { selector: ".case-study__section", reveal: "item", delayStep: 110, maxDelay: 110 },
        { selector: ".case-study__results-panel", reveal: "panel", delay: 300 },
        { selector: ".case-study__results li", reveal: "item", delayStep: 95, maxDelay: 190 },
        { selector: ".case-study__footer", delay: 420, reveal: "panel" },
        { selector: ".why-section__heading", reveal: "title" },
        { selector: ".why-stats", delay: 90, reveal: "panel" },
        {
            selector: ".advantage-row",
            reveal: "item",
            delay(index) {
                return Math.floor(index / 2) * 110;
            },
            maxDelay: 220,
        },
        { selector: ".why-section__closing", delay: 340, reveal: "panel" },
        { selector: ".final-cta", reveal: "panel" },
        { selector: ".final-cta .button", delay: 120, reveal: "button" },
        { selector: ".site-footer__inner", reveal: "soft" },
    ];

    const revealElements = [];

    revealGroups.forEach(({ selector, delayStep = 0, delay, maxDelay = 660, reveal = "up" }) => {
        const elements = document.querySelectorAll(selector);

        elements.forEach((element, index) => {
            element.classList.add("reveal-on-scroll");
            if (reveal !== "up") {
                element.dataset.reveal = reveal;
            }

            let resolvedDelay = 0;

            if (typeof delay === "function") {
                resolvedDelay = delay(index, elements);
            } else if (typeof delay === "number") {
                resolvedDelay = delay;
            } else if (delayStep > 0) {
                resolvedDelay = index * delayStep;
            }

            if (resolvedDelay > 0) {
                element.style.setProperty(
                    "--reveal-delay",
                    `${Math.min(resolvedDelay, maxDelay)}ms`,
                );
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
            threshold: 0.08,
            rootMargin: "0px 0px 10% 0px",
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
