document.addEventListener('DOMContentLoaded', function () {
const slide = document.querySelector('.carousel-slide');
const slides = Array.from(slide.children);
const totalSlides = slides.length;
let currentIndex = 0;



function typeCaption(captionElement, text) {
let index = 0;

function type() {
    if (index < text.length) {
        captionElement.textContent += text[index];
        index++;
        setTimeout(type, 100);
    }
}

type();
}


function updateCarousel() {
slide.style.transform = `translateX(-${currentIndex * 100}%)`;
const captionElement = slides[currentIndex].querySelector('.carousel-caption p');
const captionText = captionElement.textContent;
captionElement.textContent = '';
typeCaption(captionElement, captionText);
}

document.getElementById('nextBtn').addEventListener('click', function () {
currentIndex = (currentIndex + 1) % totalSlides;
updateCarousel();
});

document.getElementById('prevBtn').addEventListener('click', function () {
currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
updateCarousel();
});


setInterval(function () {
currentIndex = (currentIndex + 1) % totalSlides;
updateCarousel();
}, 5000);


updateCarousel();
});

var modal = document.getElementById('myModal');
var modalImg = document.getElementById("img01");
var images = document.getElementsByClassName('class_img');
var deleteButton = document.getElementById('deleteButton');

for (let img of images) {
img.onclick = function () {
modal.style.display = "block";
modalImg.src = this.src;
deleteButton.style.display = "block";
}
}

var span = document.getElementsByClassName("close")[0];
span.onclick = function () {
modal.style.display = "none";
deleteButton.style.display = "none";
}
deleteButton.onclick = function () {
alert("هل أنت متأكد أنك تريد حذف هذه الصورة؟");
}
