"use strict";
/**
 * GENERIC UTILITY FUNCTIONS
 */
/**
 * Convenience function that creates an `IntersectionObserver` that executes a callback passing it
 * the element that is intersecting the viewport with the greatest intersection ratio.
 */
function onIntersectChange(targetIntersectHandler, { threshold, rootMargin }) {
    return new IntersectionObserver((entries) => {
        entries
            .filter((entry) => entry.intersectionRatio > threshold)
            .sort((a, b) => b.intersectionRatio - a.intersectionRatio)
            .map((entry) => entry.target)
            .forEach((target, index) => {
            if (!index) {
                targetIntersectHandler(target);
            }
        });
    }, { threshold: [threshold], rootMargin });
}
function asyncTimeout(millis) {
    return new Promise((resolve) => {
        setTimeout(() => resolve(), millis);
    });
}
/**
 * Returns a throttled version of a given input function, which will be executed at most once
 * every `millis` milliseconds. At the end of each period, the most recent invocation will be
 * executed. Execution also happens immediately if invoked while no throttle window is in
 * progress.
 * @param {(...args: any[]) => void} func Function to be throttled
 * @param {number} millis Throttle time in milliseconds
 */
function throttle(func, millis) {
    let active;
    let lastArgs;
    let count;
    return async (...args) => {
        if (!active) {
            active = true;
            lastArgs = args;
            func(...args);
            count = 0;
            while (true) {
                await asyncTimeout(millis);
                if (count) {
                    count = 0;
                    func(...lastArgs);
                }
                else {
                    break;
                }
            }
            // eslint-disable-next-line require-atomic-updates
            active = false;
        }
        else {
            count++;
            lastArgs = args;
        }
    };
}
/**
 * Returns a debounced version of a given input function, which will be executed after `millis`
 * milliseconds of no additional invocations. Each invocation that occurs within the timing window
 * resets the timer.
 * @param func Function to be debounced
 * @param millis Debounce time in milliseconds
 * @param initial If true, the initial invocation executes immediately before the debounce
 * window begins. If no more invocations occur, the function is not executed again; otherwise
 * behaves as if `initial = false`.
 */
function debounce(func, millis, initial = false) {
    let count = 0;
    const loop = async (...args) => {
        if (!count && initial) {
            func(...args);
        }
        count++;
        const id = count;
        await asyncTimeout(millis);
        if (id === count) {
            count = 0;
            if (id > 1 || !initial) {
                func(...args);
            }
        }
    };
    return loop;
}
/**
 * Basic semver comparator. Only works with numbers, e.g. 1.2.1. Returns positive if target newer
 * than source, negative if target older than source, or zero if equal.
 * @param {string} source
 * @param {string} target
 */
function versionComparator(source, target) {
    const sourceParts = source.split('.').map((num) => parseInt(num, 10));
    const targetParts = target.split('.').map((num) => parseInt(num, 10));
    const recursor = (s, t) => {
        if (!s.length && !t.length) {
            return 0;
        }
        else if (!s.length) {
            return t[0] || 0;
        }
        else if (!t.length) {
            return -(s[0] || 0);
        }
        const diff = t[0] - s[0];
        return diff === 0 ? recursor(s.slice(1), t.slice(1)) : diff;
    };
    return recursor(sourceParts, targetParts);
}
/**
 * Creates a wrapper around `requestAnimationFrame` to enable a simpler task-based API for using
 * it.
 *
 * @see AnimationDispatcher
 */
function createAnimationDispatcher() {
    let tasks = {};
    const watchers = {};
    const loop = () => {
        for (const task of Object.values(tasks)) {
            task();
        }
        tasks = {};
        for (const watcher of Object.values(watchers)) {
            watcher();
        }
        requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
    return {
        addTask: (label, task) => {
            tasks[label] = task;
        },
        setWatcher: (label, watcher) => {
            if (!watcher) {
                delete watchers[label];
            }
            else {
                watchers[label] = watcher;
            }
        },
    };
}
/// <reference path="./types.ts" />
/**
 * CONFIGURATION AND CONSTANTS
 */
const versionCheckUrl = 'https://api.github.com/repos/luejerry/html-mangareader/contents/version';
/**
 * Key for which app data is stored in LocalStorage
 */
const storageKey = 'mangareader-config';
/**
 * Max number of pages to load at once, if `dynamicImageLoading` is enabled in `config.ini`
 */
const maxLoadedImages = 20;
/**
 * Max number of navbar previews to load at once, if `dynamicImageLoading` is enabled in
 * `config.ini`
 */
const maxLoadedPreviews = 60;
const loadingPlaceholder = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8HwYAAloBV80ot9EAAAAASUVORK5CYII=';
const smartFit = {
    size0: {
        portrait: {
            width: 720,
            height: 1024,
        },
        landscape: {
            height: 1024,
        },
        portraitLong: {
            width: 720,
        },
    },
    size1: {
        portrait: {
            width: 1080,
            height: 1440,
        },
        landscape: {
            height: 1280,
        },
        portraitLong: {
            width: 1080,
        },
    },
};
const INTERSECT_MARGIN = {
    vertical: '-45% 0px -45% 0px',
    horizontal: '0px -45% 0px -45%',
    'horizontal-rtl': '0px -45% 0px -45%',
};
/// <reference path="./types.ts" />
/// <reference path="./utils.ts" />
/// <reference path="./constants.ts" />
(function () {
    /**
     * GLOBAL VARIABLES
     */
    const pages = Array.from(document.getElementsByClassName('page'));
    const images = Array.from(document.getElementsByClassName('image'));
    const originalWidthBtn = document.getElementById('btn-original-width');
    const shrinkSizeBtn = document.getElementById('btn-shrink-size');
    const shrinkWidthBtn = document.getElementById('btn-shrink-width');
    const shrinkHeightBtn = document.getElementById('btn-shrink-height');
    const fitWidthBtn = document.getElementById('btn-fit-width');
    const fitHeightBtn = document.getElementById('btn-fit-height');
    const smartFitBtns = Array.from(document.getElementsByClassName('btn-smart-fit'));
    const directionRadioBtns = Array.from(document.getElementsByName('view-direction'));
    const smoothScrollCheckbox = document.getElementById('input-smooth-scroll');
    const darkModeCheckbox = document.getElementById('input-dark-mode');
    const invertModeCheckbox = document.getElementById('input-niggative-mode');
    const seamlessCheckbox = document.getElementById('input-seamless');
    const scrubberIconDiv = document.getElementById('scrubber-icon');
    const scrubberContainerDiv = document.getElementById('scrubber-container');
    const scrubberDiv = document.getElementById('scrubber');
    const scrubberPreviewDiv = document.getElementById('scrubber-preview');
    const scrubberMarker = document.getElementById('scrubber-marker');
    const scrubberMarkerActive = document.getElementById('scrubber-marker-active');
    let scrubberImages; // Array of images, set in `setupScrubber()`
    const animationDispatcher = createAnimationDispatcher();
    let intersectObserver;
    let visiblePage;
    let configIni = {};
    // Used by scrubber
    const scrubberState = {
        screenHeight: 0,
        previewHeight: 0,
        markerHeight: 0,
        visiblePageIndex: 0,
        previewPageIndex: 0,
        viewDirection: 'vertical',
    };
    /**
     * Read local `config.ini` file which is encoded in base64 in the `body[data-config]` attribute.
     * @returns Parsed config object, or empty object if valid config not found.
     */
    function load_config_ini() {
        try {
            return JSON.parse(atob(document.body.dataset.config || ''));
        }
        catch (e) {
            console.error('Failed to parse config.ini', e);
            return {};
        }
    }
    /**
     * Setup tasks to be run when the user scrolls to a new page.
     */
    function setupIntersectionObserver(threshold, rootMargin) {
        const throttledUpdateLoadedImages = throttle(updateLoadedImages, 1000);
        const observer = onIntersectChange((target) => {
            visiblePage = target;
            if (target.dataset.index == null) {
                return;
            }
            // Update the URL hash as user scrolls.
            const url = new URL(location.href);
            url.hash = target.id;
            history.replaceState(null, '', url.toString());
            // Update the scrubber marker as user scrolls.
            scrubberState.visiblePageIndex = parseInt(target.dataset.index, 10);
            setScrubberMarkerActive(scrubberState.visiblePageIndex);
            if (configIni.dynamicImageLoading) {
                throttledUpdateLoadedImages(images, scrubberState.visiblePageIndex, maxLoadedImages, 'pageloader');
            }
        }, { threshold, rootMargin });
        for (const page of pages) {
            observer.observe(page);
        }
        return observer;
    }
    /**
     * Load and unload images as the visible page changes with scrolling.
     * @param imgs Images to load/unload.
     * @param visiblePageIndex Index of currently visible page. Images within a distance of this page
     * are loaded, and images outside this distance are unloaded. A null value unloads all images.
     * @param maxLoad Maximum number of images to be loaded at once.
     * @param tag Task identifier, to distinguish separate usages from each other in the animation
     * scheduler.
     */
    function updateLoadedImages(imgs, visiblePageIndex, maxLoad, tag) {
        animationDispatcher.addTask(tag, () => {
            const maxDistance = maxLoad / 2;
            for (const [i, img] of imgs.entries()) {
                if (visiblePageIndex == null) {
                    img.src = loadingPlaceholder;
                }
                else if ((!img.src || img.src === loadingPlaceholder) &&
                    Math.max(visiblePageIndex - maxDistance, 0) <= i &&
                    i <= visiblePageIndex + maxDistance) {
                    img.src = img.dataset.src || loadingPlaceholder;
                }
                else if (img.src !== loadingPlaceholder &&
                    (i < visiblePageIndex - maxDistance || visiblePageIndex + maxDistance < i)) {
                    img.src = loadingPlaceholder;
                }
            }
        });
    }
    const imagesMeta = images.map((image) => {
        const ratio = image.height / image.width;
        return {
            image,
            orientation: ratio > 2 ? 'portraitLong' : ratio > 1 ? 'portrait' : 'landscape',
        };
    });
    /**
     * Read the configuration stored in browser LocalStorage. Unlike `config.ini` these settings can
     * be changed directly from the UI.
     *
     * Note that some browser security policies may forbid LocalStorage access, in which case this
     * function will return an empty object.
     *
     * @returns Parsed configuration file, or empty object if valid config not found or cannot be
     * accessed.
     */
    function readConfig() {
        let config = {};
        try {
            // Unfortunately Edge does not allow localStorage access for file:// urls
            const serializedConfig = localStorage.getItem(storageKey);
            config = JSON.parse(serializedConfig || '{}');
        }
        catch (err) {
            console.error(err);
        }
        return config;
    }
    /**
     * Update configuration to browser LocalStorage. Note that some browser security policies may
     * forbid LocalStorage access, in which case this function will do nothing.
     * @param config Configuration key-value pairs to update. Update is merged with existing config.
     */
    function writeConfig(config) {
        const oldConfig = readConfig();
        const newConfig = { ...oldConfig, ...config };
        try {
            localStorage.setItem(storageKey, JSON.stringify(newConfig));
        }
        catch (err) {
            console.error(err);
        }
    }
    /**
     * Do initial setup of the page based on configuration settings.
     */
    async function loadSettings() {
        configIni = load_config_ini();
        const config = readConfig();
        initShowNavPref(configIni);
        initScalingMode(config);
        // Need to wait for page to render, otherwise intersection observer fires before viewport
        // moves to the initial URL hash for the opened image
        await asyncTimeout(0);
        setupDirection(config);
        setupZenscroll(config);
        setupDarkMode(config);
        setupInvertMode(config);
        setupSeamless(config);
        setupScrubber(configIni);
    }
    /**
     * Hide the navigation buttons if `disable-nav = yes` in `config.ini`.
     */
    function initShowNavPref(config) {
        if (config.disableNavButtons) {
            document.body.classList.add('disable-nav');
        }
    }
    /**
     * Apply the user's last selected image scaling preference. Defaults to original size.
     */
    function initScalingMode(config) {
        const scaling = config.scaling || 'none';
        switch (scaling) {
            case 'none':
                return handleOriginalSize();
            case 'fit_width':
                return handleFitWidth();
            case 'fit_height':
                return handleFitHeight();
            case 'shrink':
                return handleShrinkSize();
            case 'shrink_width':
                return handleShrinkWidth();
            case 'shrink_height':
                return handleShrinkHeight();
            case 'smart_size0':
                return smartFitImages(smartFit.size0);
            case 'smart_size1':
                return smartFitImages(smartFit.size1);
        }
    }
    /**
     * Apply the user's last selected layout direction preference. Defaults to vertical direction.
     */
    async function setupDirection(config) {
        var _a;
        const direction = config.direction || 'vertical';
        const directionRadioBtn = directionRadioBtns.find((button) => button.value === direction);
        if (!directionRadioBtn) {
            return;
        }
        directionRadioBtn.checked = true;
        setDirection(direction);
        // HACK: on initial page load, browser auto scrolls to the beginning of the page after some
        // unspecified delay.
        // For RTL layout, viewport must be scrolled to the end initially but must be delayed until
        // after the browser scrolls. The timing is determined experimentally
        if (direction === 'horizontal-rtl') {
            await asyncTimeout(100);
            (_a = pages[0]) === null || _a === void 0 ? void 0 : _a.scrollIntoView({ inline: 'end' });
        }
    }
    /**
     * Apply the user's last selected smooth scroll preference.
     */
    function setupZenscroll(config) {
        window.zenscroll.setup(170);
        if (config.smoothScroll) {
            smoothScrollCheckbox.checked = true;
        }
        else {
            window.pauseZenscroll = true;
        }
    }
    /**
     * Apply the user's last selected dark mode preference.
     */
    function setupDarkMode(config) {
        var _a;
        darkModeCheckbox.checked = (_a = config.darkMode) !== null && _a !== void 0 ? _a : false;
        // Setting `checked` does not fire the `change` event, so we must dispatch it manually
        if (config.darkMode) {
            const change = new Event('change', { cancelable: true });
            darkModeCheckbox.dispatchEvent(change);
        }
    }

    function setupInvertMode(config) {
        var _a;
        const invertModeCheckbox = document.getElementById('input-niggative-mode');
        invertModeCheckbox.checked = (_a = config.invertMode) !== null && _a !== void 0 ? _a : false;
    
        // Apply the invert mode based on the checkbox state
        if (config.invertMode) {
            document.body.classList.add('invert-mode');
        } else {
            document.body.classList.remove('invert-mode');
        }
    
        // Add an event listener to handle changes to the invert mode checkbox
        invertModeCheckbox.addEventListener('change', (event) => {
            if (event.target.checked) {
                document.body.classList.add('invert-mode');
            } else {
                document.body.classList.remove('invert-mode');
            }
            writeConfig({ invertMode: event.target.checked });
        });
    }
    /**
     * Apply the user's last selected collapse spacing preference.
     */
    function setupSeamless(config) {
        var _a;
        seamlessCheckbox.checked = (_a = config.seamless) !== null && _a !== void 0 ? _a : false;
        if (config.seamless) {
            const change = new Event('change', { cancelable: true });
            seamlessCheckbox.dispatchEvent(change);
        }
    }
    /**
     * @returns Width of the browser viewport in pixels.
     */
    function getWidth() {
        return document.documentElement.clientWidth;
    }
    /**
     * @returns Height of the browser viewport in pixels.
     */
    function getHeight() {
        return document.documentElement.clientHeight;
    }
    function getImageHeightAttribute(img) {
        return parseInt(img.getAttribute('height') || '-1', 10);
    }
    function getImageWidthAttribute(img) {
        return parseInt(img.getAttribute('width') || '-1', 10);
    }
    /**
     * @returns Rescaled height of an image if sized to `width`, preserving aspect ratio.
     */
    function widthToRatioHeight(img, width) {
        return (width / getImageWidthAttribute(img)) * getImageHeightAttribute(img);
    }
    /**
     * @returns Rescaled width of an image if sized to `height`, preserving aspect ratio.
     */
    function heightToRatioWidth(img, height) {
        return (height / getImageHeightAttribute(img)) * getImageWidthAttribute(img);
    }
    function handleOriginalSize() {
        setImagesWidth('none', getWidth());
        writeConfig({ scaling: 'none' });
    }
    function handleShrinkSize() {
        setImagesDimensions('shrink', getWidth(), getHeight());
        writeConfig({ scaling: 'shrink' });
    }
    function handleFitWidth() {
        setImagesWidth('fit', getWidth());
        writeConfig({ scaling: 'fit_width' });
    }
    function handleFitHeight() {
        setImagesHeight('fit', getHeight());
        writeConfig({ scaling: 'fit_height' });
    }
    function handleShrinkWidth() {
        setImagesWidth('shrink', getWidth());
        writeConfig({ scaling: 'shrink_width' });
    }
    function handleShrinkHeight() {
        setImagesHeight('shrink', getHeight());
        writeConfig({ scaling: 'shrink_height' });
    }
    function handleSmartWidth(event) {
        if (event.target instanceof HTMLElement) {
            const key = event.target.dataset.fitKey;
            if (key) {
                smartFitImages(smartFit[key]);
                writeConfig({ scaling: `smart_${key}` });
            }
        }
    }
    function setImagesWidth(fitMode, width) {
        for (const img of images) {
            switch (fitMode) {
                case 'fit':
                    Object.assign(img.style, {
                        width: `${width}px`,
                        height: `${widthToRatioHeight(img, width)}px`,
                    });
                    break;
                case 'shrink':
                    const maxWidth = Math.min(getImageWidthAttribute(img), width);
                    Object.assign(img.style, {
                        width: `${maxWidth}px`,
                        height: `${widthToRatioHeight(img, maxWidth)}px`,
                    });
                    break;
                default:
                    Object.assign(img.style, {
                        width: null,
                        height: null,
                    });
            }
        }
        visiblePage === null || visiblePage === void 0 ? void 0 : visiblePage.scrollIntoView();
    }
    function setImagesHeight(fitMode, height) {
        for (const img of images) {
            switch (fitMode) {
                case 'fit':
                    Object.assign(img.style, {
                        height: `${height}px`,
                        width: `${heightToRatioWidth(img, height)}px`,
                    });
                    break;
                case 'shrink':
                    const maxHeight = Math.min(getImageHeightAttribute(img), height);
                    Object.assign(img.style, {
                        width: `${heightToRatioWidth(img, maxHeight)}px`,
                        height: `${maxHeight}px`,
                    });
                    break;
                default:
                    Object.assign(img.style, {
                        width: null,
                        height: null,
                    });
            }
        }
        visiblePage === null || visiblePage === void 0 ? void 0 : visiblePage.scrollIntoView({ inline: 'center' });
    }
    function setImagesDimensions(fitMode, width, height) {
        for (const img of images) {
            switch (fitMode) {
                case 'fit':
                    // Not implemented
                    break;
                case 'shrink':
                    clampImageSize(img, height, width);
                    break;
                default:
                    Object.assign(img.style, {
                        width: null,
                        height: null,
                    });
            }
        }
        visiblePage === null || visiblePage === void 0 ? void 0 : visiblePage.scrollIntoView();
    }
    function clampImageSize(img, height, width) {
        const scaledWidth = heightToRatioWidth(img, height);
        const scaledHeight = widthToRatioHeight(img, width);
        if (getImageHeightAttribute(img) <= height && getImageWidthAttribute(img) <= width) {
            Object.assign(img.style, {
                width: null,
                height: null,
            });
        }
        else if (scaledWidth > width) {
            Object.assign(img.style, {
                width: `${width}px`,
                height: `${scaledHeight}px`,
            });
        }
        else if (scaledHeight > height) {
            Object.assign(img.style, {
                width: `${scaledWidth}px`,
                height: `${height}px`,
            });
        }
    }
    function smartFitImages(fitMode) {
        const screenWidth = getWidth();
        const screenHeight = getHeight();
        for (const { image: img, orientation: orient } of imagesMeta) {
            switch (orient) {
                case 'portrait':
                    const maxHeight = Math.min(getImageHeightAttribute(img), fitMode.portrait.height);
                    Object.assign(img.style, {
                        width: `${heightToRatioWidth(img, maxHeight)}px`,
                        height: `${maxHeight}px`,
                    });
                    break;
                case 'landscape':
                    clampImageSize(img, Math.min(screenHeight, fitMode.landscape.height), screenWidth);
                    break;
                case 'portraitLong':
                    const maxWidth = Math.min(getImageWidthAttribute(img), fitMode.portraitLong.width);
                    Object.assign(img.style, {
                        width: `${maxWidth}px`,
                        height: `${widthToRatioHeight(img, maxWidth)}px`,
                    });
            }
        }
        visiblePage === null || visiblePage === void 0 ? void 0 : visiblePage.scrollIntoView({ inline: 'center' });
    }
    function setDirection(direction) {
        scrubberState.viewDirection = direction;
        // intersection observer must be recreated to change the root margin
        intersectObserver === null || intersectObserver === void 0 ? void 0 : intersectObserver.disconnect();
        document.body.classList.remove('vertical', 'horizontal', 'horizontal-rtl');
        document.body.classList.add(direction);
        switch (direction) {
            case 'horizontal':
            case 'horizontal-rtl':
                handleFitHeight();
            case 'vertical':
                visiblePage === null || visiblePage === void 0 ? void 0 : visiblePage.scrollIntoView({ inline: 'center' });
        }
        intersectObserver = setupIntersectionObserver(0, INTERSECT_MARGIN[direction]);
        writeConfig({
            direction: direction,
        });
    }
    function handleViewDirection(event) {
        if (!(event.target instanceof HTMLInputElement)) {
            return;
        }
        const direction = event.target.value;
        if (!direction) {
            return;
        }
        setDirection(direction);
    }
    function handleSmoothScroll(event) {
        if (!(event.target instanceof HTMLInputElement)) {
            return;
        }
        window.pauseZenscroll = !event.target.checked;
        writeConfig({
            smoothScroll: event.target.checked,
        });
    }
    function handleDarkMode(event) {
        if (!(event.target instanceof HTMLInputElement)) {
            return;
        }
        const darkModeEnabled = event.target.checked;
        if (darkModeEnabled) {
            document.body.classList.add('dark');
        }
        else {
            document.body.classList.remove('dark');
        }
        writeConfig({
            darkMode: darkModeEnabled,
        });
    }
    function handleSeamless(event) {
        if (!(event.target instanceof HTMLInputElement)) {
            return;
        }
        const seamlessEnabled = event.target.checked;
        if (seamlessEnabled) {
            document.body.classList.add('seamless');
        }
        else {
            document.body.classList.remove('seamless');
        }
        writeConfig({
            seamless: seamlessEnabled,
        });
        visiblePage === null || visiblePage === void 0 ? void 0 : visiblePage.scrollIntoView({ inline: 'center' });
    }
    function handleHorizontalScroll(event) {
        if (event.ctrlKey || event.shiftKey || event.altKey || event.metaKey || !event.deltaY) {
            return;
        }
        switch (scrubberState.viewDirection) {
            case 'horizontal':
                event.preventDefault();
                window.scrollBy({ left: event.deltaY });
                return;
            case 'horizontal-rtl':
                event.preventDefault();
                window.scrollBy({ left: -event.deltaY });
                return;
        }
    }
    function setupListeners() {
        originalWidthBtn.addEventListener('click', handleOriginalSize);
        shrinkSizeBtn.addEventListener('click', handleShrinkSize);
        shrinkWidthBtn.addEventListener('click', handleShrinkWidth);
        shrinkHeightBtn.addEventListener('click', handleShrinkHeight);
        fitWidthBtn.addEventListener('click', handleFitWidth);
        fitHeightBtn.addEventListener('click', handleFitHeight);
        for (const button of smartFitBtns) {
            button.addEventListener('click', handleSmartWidth);
        }
        for (const button of directionRadioBtns) {
            button.addEventListener('input', handleViewDirection);
        }
        smoothScrollCheckbox.addEventListener('change', handleSmoothScroll);
        darkModeCheckbox.addEventListener('change', handleDarkMode);
        seamlessCheckbox.addEventListener('change', handleSeamless);
        document.addEventListener('wheel', handleHorizontalScroll, { passive: false });
    }
    function setupScrubberPreview() {
        const previewImages = images.map((img, i) => {
            const previewImage = document.createElement('img');
            previewImage.loading = 'lazy';
            previewImage.classList.add('scrubber-preview-image');
            previewImage.dataset.index = `${i}`;
            if (configIni.dynamicImageLoading) {
                previewImage.src = loadingPlaceholder;
            }
            else {
                previewImage.src = img.dataset.thumbnail || loadingPlaceholder;
            }
            previewImage.dataset.src = `${img.dataset.thumbnail}`;
            previewImage.addEventListener('error', async (event) => {
                previewImage.src = loadingPlaceholder;
                await asyncTimeout(2000);
                previewImage.src = previewImage.dataset.src || loadingPlaceholder;
            });
            previewImage.style.width = `${heightToRatioWidth(img, 180)}px`;
            return previewImage;
        });
        scrubberPreviewDiv.append(...previewImages);
        return previewImages;
    }
    function computeMarkerY(cursorY) {
        return Math.max(0, Math.min(cursorY - scrubberState.markerHeight / 2, scrubberState.screenHeight - scrubberState.markerHeight));
    }
    function setScrubberMarkerActive(activeIndex) {
        const activeY = ((activeIndex + 0.5) / images.length) * scrubberState.screenHeight -
            scrubberState.markerHeight / 2;
        scrubberMarkerActive.style.transform = `translateY(${activeY}px)`;
        scrubberMarkerActive.innerText = `${activeIndex + 1}`;
    }
    function setupScrubber(configIni) {
        if (configIni.disableNavBar) {
            scrubberIconDiv.style.display = 'none';
            scrubberContainerDiv.style.display = 'none';
            return;
        }
        let prevImage;
        const setPreviewScroll = (cursorY) => {
            const cursorYRatio = cursorY / scrubberState.screenHeight;
            scrubberPreviewDiv.style.transform = `translateY(${-cursorYRatio * scrubberState.previewHeight + cursorY}px)`;
        };
        const setMarkerPosition = (cursorY) => {
            const markerYPos = computeMarkerY(cursorY);
            scrubberMarker.style.transform = `translateY(${markerYPos}px)`;
        };
        const setMarkerText = (text) => {
            scrubberMarker.innerText = text;
        };
        const debouncedUpdateLoadedImages = debounce(updateLoadedImages, 0);
        let scrubberActivated = false;
        scrubberDiv.addEventListener('mouseenter', () => {
            if (!scrubberActivated) {
                scrubberImages = setupScrubberPreview();
                scrubberActivated = true;
            }
            scrubberState.screenHeight = document.documentElement.clientHeight;
            // We can't style this as 100vh because it doesn't account for horizontal scrollbar
            scrubberState.previewHeight = scrubberPreviewDiv.offsetHeight;
            scrubberState.markerHeight = scrubberMarker.offsetHeight;
            setScrubberMarkerActive(scrubberState.visiblePageIndex);
            scrubberDiv.style.height = `${scrubberState.screenHeight}px`;
            scrubberContainerDiv.style.opacity = '1';
        });
        scrubberDiv.addEventListener('mouseleave', () => {
            scrubberContainerDiv.style.opacity = '0';
            if (configIni.dynamicImageLoading) {
                updateLoadedImages(scrubberImages, null, maxLoadedPreviews, 'scrubber');
            }
        });
        scrubberDiv.addEventListener('mousemove', (event) => {
            var _a;
            const cursorY = event.clientY;
            const cursorYRatio = cursorY / scrubberState.screenHeight;
            scrubberState.previewPageIndex = Math.floor(cursorYRatio * images.length);
            if (configIni.dynamicImageLoading) {
                debouncedUpdateLoadedImages(scrubberImages, scrubberState.previewPageIndex, maxLoadedPreviews, 'scrubber');
            }
            const image = scrubberImages[scrubberState.previewPageIndex];
            if (!image) {
                return;
            }
            if (event.buttons & 1) {
                // Allow left click drag scrubbing
                if (scrubberState.previewPageIndex !== scrubberState.visiblePageIndex) {
                    (_a = images[scrubberState.previewPageIndex]) === null || _a === void 0 ? void 0 : _a.scrollIntoView({ inline: 'center' });
                }
            }
            animationDispatcher.addTask('mousemove', () => {
                setMarkerPosition(cursorY);
                setMarkerText(`${scrubberState.previewPageIndex + 1}`);
                setPreviewScroll(cursorY);
                if (prevImage !== image) {
                    image.classList.add('hovered');
                    if (prevImage) {
                        prevImage.classList.remove('hovered');
                    }
                    prevImage = image;
                }
            });
        });
        scrubberDiv.addEventListener('click', (event) => {
            var _a;
            const cursorYRatio = event.clientY / scrubberState.screenHeight;
            const imageIndex = Math.floor(cursorYRatio * images.length);
            (_a = images[imageIndex]) === null || _a === void 0 ? void 0 : _a.scrollIntoView({ inline: 'center' });
        });
    }
    async function checkVersion() {
        const response = await fetch(versionCheckUrl, { method: 'GET', mode: 'cors' }).then((r) => r.json());
        const remoteVersion = atob(response.content);
        const versionDiv = document.getElementById('version');
        const localVersion = versionDiv.innerText;
        const compare = versionComparator(localVersion, remoteVersion);
        if (compare > 0) {
            const nextVersionSpan = document.getElementById('next-version');
            const linkUpdate = document.getElementById('link-update');
            const updateToast = document.getElementById('update-toast');
            nextVersionSpan.innerText = remoteVersion;
            linkUpdate.href = 'https://github.com/Kurdeus/Comic-Reader/releases';
            Object.assign(updateToast.style, { display: 'initial' });
            await asyncTimeout(0);
            updateToast.classList.add('show');
            await asyncTimeout(5000);
            updateToast.classList.remove('show');
        }
    }
    async function main() {
        setupListeners();
        loadSettings();
        checkVersion();
    }
    main();
})();
