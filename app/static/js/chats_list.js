function showButtons() {
    $('#selected_chat .listed-chat-buttons:first').css(
        'left', String(parseFloat($('#selected_chat .listed-chat-title:first').css('width')) - 21).concat('px'))
    $('#selected_chat .listed-chat-buttons:first').css('width', '100%').addClass('show')
    $('#listed_chats_container .listed-chat').css('width', '100%')
    $('#add_chat').css('width', '100%')
    return false
}
function hideButtons() {
    if ($('#selected_chat').get(0) != null) {
        $('#selected_chat .listed-chat-buttons:first').removeClass('show').css('width', '0')
        $('#listed_chats_container .listed-chat').css('width', '0')
        $('#add_chat').css('width', '0')
    }
    return false
}

function selectChat(elem) {
    let selectedChat = $('#selected_chat').get(0)
    if (selectedChat) {
        $('#selected_chat .listed-chat-title:first').get(0).setAttribute('data-bs-target', '')
        $('#selected_chat .listed-chat-title:first').get(0).setAttribute('data-bs-toggle', '')
        $('#selected_chat .listed-chat-title:first').attr('onmouseenter', '')
        $('#selected_chat').insertBefore('#listed_chats_container .listed-chat:first')
        $('#selected_chat').attr('onclick', 'selectChat(this)')
        selectedChat.id = 'prev_selected_chat'
    }
    elem.id = 'selected_chat'
    $('#selected_chat').attr('onclick', '')
    $('#selected_chat').insertBefore('#listed_chats_container')
    $('#selected_chat .listed-chat-title:first').attr('onmouseenter', 'showButtons()')
    $('#selected_chat .listed-chat-title:first').get(0).setAttribute('data-bs-toggle', 'modal')
    $('#selected_chat .listed-chat-title:first').get(0).setAttribute('data-bs-target', '#chat_title_modal')
    if ($('#prev_selected_chat').get(0) && $(
      '#prev_selected_chat .listed-chat-buttons:first').attr('class').search('show')) {
        $('#prev_selected_chat .listed-chat-buttons:first').removeClass('show').css('width', '0')
        $('#prev_selected_chat').attr('id', '')
    }
    return false
}

function prepareForTitleModal() {
    if ($($(this).get(0).parentElement).attr('id') == 'selected_chat') {
        $(this).attr('data-bs-toggle', 'modal')
        $(this).attr('data-bs-target', '#chat_title_modal')
    }
    return false
}

var chatsData = new Array()
function saveChatData(attr) {
    let value = $(`#chat_${attr}_modal_input`)
    if (attr == 'description') {
        value = value.text()
    } else {
        value = value.val()
    }
    if (typeof chatsData[parseInt($(`#chat_${attr}_modal_id`).val())] === 'undefined') {
        chatsData[parseInt($(`#chat_${attr}_modal_id`).val())] = new Object()
    }
    let chatData = chatsData[parseInt($(`#chat_${attr}_modal_id`).val())]
    if (attr == 'title') {
        chatData.title = value
    } else if (attr == 'description') {
        chatData.description = value
    }
    return false
}

function updateChatModalData(attr) {
    if ($(`#chat_${attr}_modal`).css('display') != 'none') {
        let chatData = chatsData[parseInt($(`#chat_${attr}_modal_id`).val())]
        if (typeof chatData !== 'undefined') {
            let value = null
            if (attr == 'title') {
                value = chatData.title
            } else if (attr == 'description') {
                value = chatData.description
            }
            if (value != null) {
                if (attr == 'description') {
                    $(`#chat_${attr}_modal_input`).text(value)
                } else {
                    $(`#chat_${attr}_modal_input`).val(value)
                }
            }
        }
    }
    return false
}

function showChatModalAlert(attr) {
    let alert = $(`#chat_${attr}_modal_alert`)
    alert.fadeIn(350)
    setTimeout(function() {alert.fadeOut(350); return false}, 2000)
    return false
}

function showChatModalAlertOnStatus(attr, status, func, status2=null, attr2=null) {
    setTimeout(function () {
        console.log(lastResponseStatus)
        if (lastResponseStatus == status) {
            showChatModalAlert(attr)
        } else if (lastResponseStatus == status2) {
            showChatModalAlert(attr2)
        }
    }, 300)
}

function showChatMembersText() {
    if (document.getElementById('chat_members_text'
    ).parentElement != document.getElementById('chat_members_modal_list')) {
        var addText = true
        $('#chat_members_modal_list .chat-member-form').each(
        function () {
            if ($(this).css('display') != 'none') {
                addText = false
            }
        })
        if (addText) {
            $('#chat_members_modal_list').append($('#chat_members_text'))
        }
    }
}

var chatMembersFuncRunning = false
function showHideChatMembers() {
    if (!chatMembersFuncRunning) {
        chatMembersFuncRunning = true
        chatId = $('#chat_members_modal_id').val()
        for (let memberId = 1; memberId < 1001; memberId++) {
            let chatMemberKey = `chat_member_${chatId}_${memberId}_hidden`
            let chatMemberHidden = sessionStorage.getItem(chatMemberKey)
            if (chatMemberHidden) {
                $(`#chat_member_form_${chatId}_${memberId}`).hide()
                showChatMembersText()
            } else {
                sessionStorage.removeItem(chatMemberKey)
            }
        }
        chatMembersFuncRunning = false
    }
}

$(document).ready(function() {
    $('.listed-chat').attr('onclick', 'selectChat(this)')
    $('.chat-modal-alert').fadeOut(1)

    $('.custom-form').on('submit', function (e) {
        e.preventDefault()
        return false
    })

    $('.custom-input').on('keydown', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault()
            $('#' + $(this).attr('id').replace(/_[^_]+$/, `_btn`)).click()
            return false
        }
    })

    $('.modal').on('hide.bs.modal', function () {
        $(this).blur()
    })

    return false
})
