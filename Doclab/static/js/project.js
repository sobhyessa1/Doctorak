document.addEventListener('DOMContentLoaded', function () {
    var textArray = [
        "بياناتك الصحية في مكان واحد",
        "فحص التحاليل الطبيه"
    ];
    var currentIndex = 0;

    function typeText(element, text, index, callback) {
        if (index < text.length) {
            element.textContent += text[index];
            setTimeout(function () {
                typeText(element, text, index + 1, callback);
            }, 100); // ضبط سرعة الكتابة هنا
        } else if (callback) {
            setTimeout(callback, 1000); // تأخير قبل بدء النص التالي
        }
    }

    function startTyping(index) {
        var typedTextElement = document.querySelector('.carousel-item:nth-of-type(' + (index + 1) + ') .carousel-caption p');
        typedTextElement.textContent = ''; // مسح النص السابق
        var text = textArray[index];
        typeText(typedTextElement, text, 0, function () {
            // currentIndex = (currentIndex + 1) % textArray.length; // قم بإلغاء التعليق إذا كنت ترغب في التنقل خلال جميع النصوص
        });
    }

    var carousel = document.getElementById('carouselExampleCaptions');
    carousel.addEventListener('slid.bs.carousel', function (event) {
        var activeIndex = event.to;
        startTyping(activeIndex);
    });

    startTyping(0); // تهيئة للشريحة الأولى
});








