document.addEventListener("DOMContentLoaded", function () {
    class StickyNavigation {
        constructor() {
            this.currentId = null;
            this.currentTab = null;
            this.tabContainerHeight = 70;
            let self = this;

            $('.et-hero-tab').click(function (event) {
                self.onTabClick(event, $(this));
            });

            $(window).scroll(() => { this.onScroll(); });
            $(window).resize(() => { this.onResize(); });
            window.addEventListener('popstate', () => { this.onPopState(); });
        }

        onTabClick(event, element) {
            event.preventDefault();
            let targetId = element.attr('href');
            this.scrollToSection(targetId);

            // Cambiar la URL sin recargar la página
            history.pushState(null, null, targetId);
        }

        onScroll() {
            this.checkTabContainerPosition();
            this.findCurrentTabSelector();

            // Obtener el id de la sección actualmente visible
            let visibleSectionId = this.getVisibleSectionId();
            if (visibleSectionId) {
                // Cambiar la URL sin recargar la página
                history.replaceState(null, null, visibleSectionId);
            }
        }

        onResize() {
            if (this.currentId) {
                this.setSliderCss();
            }
        }

        onPopState() {
            let targetId = window.location.hash;
            this.scrollToSection(targetId);
        }

        scrollToSection(targetId) {
            let $targetSection = $(targetId);
            if ($targetSection.length > 0) {
                // Cerrar todos los acordeones
                $('.collapsibles-wrapper').removeClass('collapsible-tab__open');
                $('.collapsible-content').css('height', 0);

                // Abrir el acordeón en la sección específica
                let $collapsibleWrapper = $targetSection.find('.collapsibles-wrapper');
                $collapsibleWrapper.addClass('collapsible-tab__open');
                $collapsibleWrapper.find('.collapsible-content').css('height', 'auto');

                // Desplazar a la sección
                let scrollTop = $targetSection.offset().top - $('.et-hero-tabs-container').outerHeight(true) + 1;
                $('html, body').animate({ scrollTop: scrollTop }, 600);
            }
        }

        checkTabContainerPosition() {
            let offset = $('.et-hero-tabs').offset().top + $('.et-hero-tabs').height() - this.tabContainerHeight;
            if ($(window).scrollTop() > offset) {
                $('.et-hero-tabs-container').addClass('et-hero-tabs-container--top');
            } else {
                $('.et-hero-tabs-container').removeClass('et-hero-tabs-container--top');
            }
        }

        findCurrentTabSelector() {
            let newCurrentId;
            let newCurrentTab;
            let self = this;
            $('.et-hero-tab').each(function () {
                let id = $(this).attr('href');
                let offsetTop = $(id).offset().top - self.tabContainerHeight;
                let offsetBottom = $(id).offset().top + $(id).height() - self.tabContainerHeight;
                if ($(window).scrollTop() > offsetTop && $(window).scrollTop() < offsetBottom) {
                    newCurrentId = id;
                    newCurrentTab = $(this);
                }
            });
            if (this.currentId !== newCurrentId || this.currentId === null) {
                this.currentId = newCurrentId;
                this.currentTab = newCurrentTab;
                this.setSliderCss();
            }
        }

        setSliderCss() {
            let width = 0;
            let left = 0;
            if (this.currentTab) {
                width = this.currentTab.css('width');
                left = this.currentTab.offset().left;
            }
            $('.et-hero-tab-slider').css('width', width);
            $('.et-hero-tab-slider').css('left', left);
        }

        getVisibleSectionId() {
            let visibleSectionId = null;
            let self = this;

            $('.et-slide').each(function () {
                let id = '#' + $(this).attr('id');
                let offsetTop = $(id).offset().top - self.tabContainerHeight;
                let offsetBottom = $(id).offset().top + $(id).height() - self.tabContainerHeight;
                if ($(window).scrollTop() > offsetTop && $(window).scrollTop() < offsetBottom) {
                    visibleSectionId = id;
                }
            });

            return visibleSectionId;
        }
    }

    new StickyNavigation();
});
