// JavaScript to handle copy-to-clipboard
document.getElementById('copy-token').addEventListener('click', function() {
    const tokenText = document.getElementById('access-token').innerText;
    navigator.clipboard.writeText(tokenText).then(function() {
        alert('Token copied to clipboard!');
    }).catch(function(err) {
        alert('Failed to copy token: ', err);
    });
});