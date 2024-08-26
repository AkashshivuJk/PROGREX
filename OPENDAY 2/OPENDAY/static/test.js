const cursor = document.querySelector('.cursor');

document.addEventListener('mousemove', (e) => {
    cursor.style.left = e.clientX + 'px';
    cursor.style.top = e.clientY + 'px';

    // Calculate background color based on cursor position
    const width = window.innerWidth;
    const height = window.innerHeight;
    const x = e.clientX / width;
    const y = e.clientY / height;
    
    // Convert position to a color
    const red = Math.round(x * 255);
    const green = Math.round(y * 255);
    const blue = Math.round((1 - x) * 255);

    document.body.style.backgroundColor = `rgb(${red}, ${green}, ${blue})`;
});
