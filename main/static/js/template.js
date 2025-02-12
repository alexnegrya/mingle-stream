chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    // Process the message
    if (message.action === "something") {
        sendResponse({ success: true }); // Always respond
    }
    return true; // Keep the message channel open for async responses
});
