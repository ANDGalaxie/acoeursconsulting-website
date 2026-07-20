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

    const isCompactMotion = window.innerWidth < 768;
    const staggerStep = isCompactMotion ? 120 : 160;

    const revealGroups = [
        { selector: ".about-section__copy", reveal: "title", repeat: true },
        { selector: ".about-section__visual", reveal: "image-right", delay: 180, repeat: true },
        { selector: ".about-capability", reveal: "item", delayStep: staggerStep, maxDelay: 480, repeat: true },
        { selector: ".stage-section .section-heading", reveal: "title", repeat: true },
        { selector: ".stage-card", reveal: "item", delayStep: staggerStep, maxDelay: 480, repeat: true },
        { selector: ".service-feature", reveal: "panel", repeat: true },
        {
            selector: ".service-item",
            reveal: "item",
            repeat: true,
            delay(index) {
                const rowDelay = isCompactMotion ? 120 : 200;
                return Math.floor(index / 2) * rowDelay + (index % 2) * 40;
            },
            maxDelay: 240,
        },
        { selector: ".home-section--personal .section-heading", reveal: "title", repeat: true },
        { selector: ".personal-panel", reveal: "panel", delay: 90, repeat: true },
        { selector: ".personal-item", reveal: "item", delayStep: isCompactMotion ? 110 : 140, maxDelay: 280, repeat: true },
        { selector: ".process-section .section-heading", reveal: "title", repeat: true },
        { selector: ".process-timeline", reveal: "panel", delay: 120, repeat: true },
        { selector: ".process-stage", reveal: "item", delayStep: staggerStep, maxDelay: 640, repeat: true },
        { selector: ".process-section .section-actions", delay: 760, maxDelay: 760, reveal: "button", repeat: true },
        { selector: ".case-study__intro", reveal: "title", repeat: true },
        { selector: ".case-study__visual", reveal: "image-left", delay: 220, repeat: true },
        { selector: ".case-overview__content", reveal: "panel", delay: 420, repeat: true },
        { selector: ".case-study__section", reveal: "item", delayStep: 160, maxDelay: 160, repeat: true },
        { selector: ".case-study__results-panel", reveal: "panel", delay: 620, repeat: true },
        { selector: ".case-study__results li", reveal: "item", delayStep: 150, maxDelay: 300, repeat: true },
        { selector: ".case-study__footer", delay: 900, maxDelay: 900, reveal: "panel", repeat: true },
        { selector: ".why-section__heading", reveal: "title", repeat: true },
        { selector: ".why-stats", delay: 160, reveal: "panel", repeat: true },
        {
            selector: ".advantage-row",
            reveal: "item",
            repeat: true,
            delay(index) {
                const rowDelay = isCompactMotion ? 120 : 200;
                return Math.floor(index / 2) * rowDelay;
            },
            maxDelay: 400,
        },
        { selector: ".why-section__closing", delay: 620, maxDelay: 620, reveal: "panel", repeat: true },
        { selector: ".final-cta", reveal: "panel", repeat: true },
        { selector: ".final-cta .button", delay: 180, maxDelay: 180, reveal: "button", repeat: true },
        { selector: ".site-footer__inner", reveal: "soft", repeat: true },
    ];

    const revealElements = [];
    const repeatElements = new Set();
    const seenElements = new Set();

    revealGroups.forEach(({ selector, delayStep = 0, delay, maxDelay = 660, reveal = "up", repeat = false }) => {
        const elements = document.querySelectorAll(selector);

        elements.forEach((element, index) => {
            if (seenElements.has(element)) {
                return;
            }

            seenElements.add(element);
            element.classList.add("reveal-on-scroll");
            if (reveal !== "up") {
                element.dataset.reveal = reveal;
            }
            if (repeat) {
                element.dataset.revealRepeat = "true";
                repeatElements.add(element);
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

    document.querySelectorAll("[data-reveal]").forEach((element) => {
        if (seenElements.has(element)) {
            return;
        }

        seenElements.add(element);
        element.classList.add("reveal-on-scroll");

        if (element.dataset.revealRepeat === "true") {
            repeatElements.add(element);
        }

        if (element.dataset.revealDelay) {
            element.style.setProperty("--reveal-delay", `${element.dataset.revealDelay}ms`);
        }

        revealElements.push(element);
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

    const resetRevealElement = (element) => {
        if (prefersReducedMotion.matches || !element.classList.contains("is-visible")) {
            return;
        }

        element.classList.add("is-resetting");
        element.classList.remove("is-visible");

        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                element.classList.remove("is-resetting");
            });
        });
    };

    const revealObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting || entry.intersectionRatio < 0.16) {
                    return;
                }

                entry.target.classList.add("is-visible");

                if (!repeatElements.has(entry.target)) {
                    revealObserver.unobserve(entry.target);
                }
            });
        },
        {
            threshold: [0, 0.16],
            rootMargin: "0px 0px -6% 0px",
        },
    );

    const resetObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (!repeatElements.has(entry.target) || entry.isIntersecting) {
                    return;
                }

                const { top, bottom } = entry.boundingClientRect;
                const viewportHeight = window.innerHeight || document.documentElement.clientHeight;
                const isFullyOutOfView = bottom <= 0 || top >= viewportHeight;

                if (isFullyOutOfView) {
                    resetRevealElement(entry.target);
                }
            });
        },
        {
            threshold: 0,
            rootMargin: "0px",
        },
    );

    revealElements.forEach((element) => {
        revealObserver.observe(element);
        if (repeatElements.has(element)) {
            resetObserver.observe(element);
        }
    });
};

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setupRevealAnimations, { once: true });
} else {
    setupRevealAnimations();
}
