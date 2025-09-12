$(document).on("submit", "form.ajax", function (e) {
    e.preventDefault();
    let $form = $(this);

    $.ajax({
        type: $form.attr("method"),
        url: $form.attr("action") || window.location.href,
        data: $form.serialize(),
        success: function (response) {
            let data = JSON.parse(response);

            if (data.status === "true") {
                Swal.fire({
                    title: data.title,
                    html: `<p class="swal-text">${data.message}</p>`,
                    icon: "success",
                    confirmButtonText: "🎉 Awesome",
                    customClass: {
                        popup: "modern-card",
                        title: "modern-title",
                        htmlContainer: "modern-text",
                        confirmButton: "modern-btn success-btn",
                        icon: "modern-icon",
                    },
                    buttonsStyling: false,
                    showClass: {
                        popup: "animate__animated animate__fadeInUp animate__faster"
                    },
                    hideClass: {
                        popup: "animate__animated animate__fadeOutDown animate__faster"
                    }
                });
                $form.trigger("reset");
            } else {
                Swal.fire({
                    title: data.title,
                    html: `<p class="swal-text">Please check your input and try again.</p>`,
                    icon: "error",
                    confirmButtonText: "⚡ Retry",
                    customClass: {
                        popup: "modern-card",
                        title: "modern-title",
                        htmlContainer: "modern-text",
                        confirmButton: "modern-btn error-btn",
                        icon: "modern-icon",
                    },
                    buttonsStyling: false,
                    showClass: {
                        popup: "animate__animated animate__shakeX animate__faster"
                    }
                });
            }
        },
        error: function () {
            Swal.fire({
                title: "Server Error",
                html: `<p class="swal-text">Something went wrong. Please try again later.</p>`,
                icon: "error",
                confirmButtonText: "💔 Close",
                customClass: {
                    popup: "modern-card",
                    title: "modern-title",
                    htmlContainer: "modern-text",
                    confirmButton: "modern-btn error-btn",
                    icon: "modern-icon",
                },
                buttonsStyling: false,
                showClass: {
                    popup: "animate__animated animate__zoomIn animate__faster"
                },
                hideClass: {
                    popup: "animate__animated animate__zoomOut animate__faster"
                }
            });
        }
    });
});