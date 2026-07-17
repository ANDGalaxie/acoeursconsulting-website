const navToggle = document.querySelector("[data-nav-toggle]");
const navPanel = document.querySelector("[data-nav-panel]");
const siteHeader = document.querySelector("[data-site-header]");

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
