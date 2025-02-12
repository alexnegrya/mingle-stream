function setImageModalArgs(model, imgUrl, args=null) {
    $('#image_modal_model').attr('value', model)
    $('#image_modal_img').attr('src', imgUrl)
    $('#image_modal_args').attr('value', args)
}

// function showFullscreenImage() {
//     document.getElementById('image_modal_fullscreen_img').style.display = 'block'
// }
