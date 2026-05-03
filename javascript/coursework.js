// collections of pdf files
const collections = {
    computer_programming: [
        {
            url: "pdfs/computer_programming/cop3035_homework5_redacted.pdf#view=FitH",
            img: "images/computer_programming/cop3035_homework5_redacted.jpg"
        },
        {
            url: "pdfs/computer_programming/cop3035_homework4_redacted.pdf#view=FitH",
            img: "images/computer_programming/cop3035_homework4_redacted.jpg"
        },
        {
            url: "pdfs/computer_programming/cop3035_homework3_redacted.pdf#view=FitH",
            img: "images/computer_programming/cop3035_homework3_redacted.jpg"
        },
        {
            url: "pdfs/computer_programming/cop3035_homework2_redacted.pdf#view=FitH",
            img: "images/computer_programming/cop3035_homework2_redacted.jpg"
        }
    ],
    computer_engineering: [
        {
            url: "pdfs/computer_engineering/Lab3_JosephLeone_redacted.pdf#view=FitH",
            img: "images/computer_engineering/Lab3_JosephLeone_redacted.jpg"
        },
        {
            url: "pdfs/computer_engineering/Lab1B_JosephLeone_redacted.pdf#view=FitH",
            img: "images/computer_engineering/Lab1B_JosephLeone_redacted.jpg"
        },
        {
            url: "pdfs/computer_engineering/Lab1A_JosephLeone_redacted.pdf#view=FitH",
            img: "images/computer_engineering/Lab1A_JosephLeone_redacted.jpg"
        }        
    ],
    data_intelligence: []
};

let current_index = 0;


// function to load a specific category
function load_gallery(category) {
    current_collection = collections[category];
    current_index = 0;
    update_viewer();
}


// function to handle arrow clicks
function change_item(direction) {
    if (current_collection.length === 0) return;
    
    current_index += direction;

    // Loop back to start/end
    if (current_index >= current_collection.length) current_index = 0;
    if (current_index < 0) current_index = current_collection.length - 1;

    update_viewer();
}


// function to update the iframe
function update_viewer() {
    const item = current_collection[current_index];
    document.getElementById('main-viewer').src = item.url;
    document.getElementById("mobile-viewer").src = item.img

    // update download link
    const donwload_link = document.getElementById("mobile-download")
    donwload_link.href = item.url.split("#")[0]

    file_number_text = "File " + String(current_index + 1) + " of " + String(current_collection.length)
    document.getElementById("file-number").textContent = file_number_text
}


window.addEventListener('DOMContentLoaded', () => {
    load_gallery("computer_programming");

    const gallery_nav = document.querySelector('#gallery-nav');
    const gallery_container = document.querySelector('#gallery-container');

    gallery_nav.addEventListener('click', (e) => {
        if (e.target.classList.contains('gallery-nav-button')) {
            const category = e.target.getAttribute("data-category")
            load_gallery(category)
        }

        if (e.target.classList.contains('nav-arrow')) {
            const direction = e.target.getAttribute("data-direction")
            if (direction == "left") {
                change_item(-1)
            }
            else {
                change_item(1)
            }
        }
    });

    
});
