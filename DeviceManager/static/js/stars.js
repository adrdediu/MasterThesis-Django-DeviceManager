import * as THREE from 'https://threejsfundamentals.org/threejs/resources/threejs/r127/build/three.module.js';

// Get the homepageDisplayArea and the canvas
var homepageDisplayArea = document.getElementById('homepageDisplayArea');
var canvas = document.getElementById('starrySky');
var renderer;

// Function to update the canvas size
function updateCanvasSize() {
    canvas.width = homepageDisplayArea.clientWidth;
    canvas.height = homepageDisplayArea.clientHeight;
    console.log(canvas.height + " " + canvas.width)
    // Update Three.js renderer size
    if (renderer) {
        renderer.setSize(canvas.width, canvas.height);
    }

    // Call your function to redraw/render the starry sky
    redrawStarrySky();
}

// Initial update
updateCanvasSize();

// Listen for window resize event
window.addEventListener('resize', updateCanvasSize);

// Example Three.js functions (replace with your own logic)
function redrawStarrySky() {
    // Initialize Three.js scene
    const scene = new THREE.Scene();

    // Create a camera
    const camera = new THREE.PerspectiveCamera(75, canvas.width / canvas.height, 0.1, 1000);
    camera.position.z = 5;

    // Create a renderer
    renderer = new THREE.WebGLRenderer({ canvas: canvas });
    renderer.setSize(canvas.width, canvas.height);

    // Create stars
    const starsGeometry = new THREE.BufferGeometry();
    const starsMaterial = new THREE.PointsMaterial({ color: 0xFFFFFF, size: 0.1 });

    const starsVertices = [];
    for (let i = 0; i < 5000; i++) {
        const x = (Math.random() - 0.5) * 2000;
        const y = (Math.random() - 0.5) * 2000;
        const z = (Math.random() - 0.5) * 2000;
        starsVertices.push(x, y, z);
    }

    starsGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starsVertices, 3));
    const stars = new THREE.Points(starsGeometry, starsMaterial);

    // Add stars to the scene
    scene.add(stars);

    // Function to animate the scene
    function animate() {
        requestAnimationFrame(animate);

        // Rotate stars
        stars.rotation.x += 0.0005;
        stars.rotation.y += 0.0005;

        // Render the scene
        renderer.render(scene, camera);
    }

    // Call the animate function
    animate();
}