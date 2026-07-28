// 3D Car Scene implementation using Three.js & OrbitControls
window.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('car-scene-container');
  const canvas = document.getElementById('car-scene-canvas');
  if (!container || !canvas) return;

  const frustratedComments = [
    "Need parking space or I'm starting\na carpool on the roof.",
    "Why do all roads lead to 'no parking'?",
    "In search of my happy place...\nAKA a parking spot.",
    "Should've bought a helicopter instead.",
    "If I had a dime for every spot taken,\nI'd own the parking lot.",
    "Brb, circling the lot for the 100th time.",
    "Finding a soulmate seems easier\nthan finding a parking spot.",
    "I came, I saw... I circled the lot.",
    "In a relationship with the 'P' sign.",
    "Growing old waiting for a parking spot.",
    "Looking for a parking spot,\nsend help.",
    "Siri, find me the nearest parking spot,\nplease!",
    "I've got 99 problems,\nand parking is all of them.",
    "Park anywhere, they said.\nIt'll be easy, they said."
  ];

  // 1. Scene Setup
  const scene = new THREE.Scene();
  
  // 2. Camera Setup (Original Overhead View)
  const camera = new THREE.PerspectiveCamera(60, container.clientWidth / container.clientHeight, 0.1, 1000);
  camera.position.set(0, 200, 0);

  // 3. Renderer Setup
  const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
  renderer.setSize(container.clientWidth, container.clientHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

  // 4. Main Yellow Searching Car (The Focus Point of the 3D Scene)
  function createCar(color = 0x888888, isYellow = false) {
    const group = new THREE.Group();
    const carColor = isYellow ? 0xedd000 : color;

    // Car Body: length=4.4 along X-axis, height=0.6, width=2.1 along Z-axis (forward aligned)
    const geo = new THREE.BoxGeometry(4.4, 0.6, 2.1);
    const mat = new THREE.MeshBasicMaterial({ color: carColor });
    const carMesh = new THREE.Mesh(geo, mat);
    carMesh.position.y = 0.3;
    group.add(carMesh);

    // Headlights
    const lightGeo = new THREE.PlaneGeometry(1.8, 3.5);
    const lightMat = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.25 });
    const headlight = new THREE.Mesh(lightGeo, lightMat);
    headlight.rotation.x = -Math.PI / 2;
    headlight.position.set(3.5, 0.05, 0);
    group.add(headlight);

    return group;
  }

  const mainCar = createCar(0xedd000, true);
  mainCar.position.set(0, 0, 9);
  scene.add(mainCar);

  // 5. OrbitControls Setup - Focused on Yellow Car, 360° Rotatable from Any Dimension
  const controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.rotateSpeed = 0.9;
  controls.zoomSpeed = 1.2;
  controls.enablePan = false; // Keep focus locked on yellow car
  
  // Set yellow car at (0, 0, 9) as the focus target
  controls.target.set(0, 0, 9);
  
  // Allow full 360-degree rotation horizontally from any angle
  controls.minAzimuthAngle = -Infinity;
  controls.maxAzimuthAngle = Infinity;
  
  // Allow vertical tilting from top-down to ground level
  controls.minPolarAngle = 0.01;
  controls.maxPolarAngle = Math.PI / 2 - 0.02;
  
  // Zoom range centered on yellow car
  controls.minDistance = 25;
  controls.maxDistance = 250;

  // 6. Lighting
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.9);
  scene.add(ambientLight);

  const dirLight = new THREE.DirectionalLight(0xffffff, 0.6);
  dirLight.position.set(100, 200, 100);
  scene.add(dirLight);

  // 7. Road Plane
  const roadGeo = new THREE.PlaneGeometry(1000, 22);
  const roadMat = new THREE.MeshBasicMaterial({ color: 0x222222 });
  const road = new THREE.Mesh(roadGeo, roadMat);
  road.position.set(-120, -0.02, -0.5);
  road.rotation.x = -Math.PI / 2;
  scene.add(road);

  // 8. World Dimensions & Spawning System
  const worldStart = -500;
  const worldEnd = 300;
  const movingObjects = [];

  function createBuildingSet(maxHeight = 20) {
    const group = new THREE.Group();
    const floorHeight = 4;
    const numBuildings = 6 + Math.floor(Math.random() * 4);
    
    for (let i = 0; i < numBuildings; i++) {
      const floors = 2 + Math.floor(Math.random() * maxHeight);
      const width = 10 + Math.random() * 15;
      const length = 10 + Math.random() * 15;
      const height = floors * floorHeight;

      const posX = (Math.random() - 0.5) * 40;
      const posZ = (Math.random() - 0.5) * 40;

      const geo = new THREE.BoxGeometry(width, height, length);
      const mat = new THREE.MeshBasicMaterial({ color: 0x333333, wireframe: true });
      const building = new THREE.Mesh(geo, mat);
      building.position.set(posX, height / 2, posZ);
      group.add(building);

      const roofGeo = new THREE.PlaneGeometry(width, length);
      const roofMat = new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.5 });
      const roof = new THREE.Mesh(roofGeo, roofMat);
      roof.position.set(posX, height, posZ);
      roof.rotation.x = -Math.PI / 2;
      group.add(roof);
    }
    return group;
  }

  const spawners = [
    { z: 192, interval: 3.6, type: 'building', maxHeight: 4 },
    { z: 72, interval: 3.6, type: 'building', maxHeight: 12 },
    { z: -73, interval: 3.6, type: 'building', maxHeight: 12 },
    { z: -193, interval: 3.6, type: 'building', maxHeight: 4 },
    { z: -10, interval: 8, type: 'car', color: 0x666666, speed: 30 },
    { z: -6, interval: 4.3, type: 'car', color: 0x888888, speed: 35 },
    { z: -2, interval: 7, type: 'car', color: 0x777777, speed: 32 },
    { z: 2, interval: 9, type: 'car', color: 0x999999, speed: -28 },
    { z: 6, interval: 7, type: 'car', color: 0x888888, speed: -32 },
    { z: 12, interval: 6, type: 'car', color: 0xaaaaaa, speed: 25 },
    { z: -13, interval: 7.3, type: 'car', color: 0x888888, speed: 25 },
  ];

  // Blinking parking slot outline under main yellow car
  const slotGeo = new THREE.BufferGeometry();
  const slotVertices = new Float32Array([
    -2.4, 0.05, -1.25,   2.4, 0.05, -1.25,
     2.4, 0.05, -1.25,   2.4, 0.05,  1.25,
     2.4, 0.05,  1.25,  -2.4, 0.05,  1.25,
    -2.4, 0.05,  1.25,  -2.4, 0.05, -1.25
  ]);
  slotGeo.setAttribute('position', new THREE.BufferAttribute(slotVertices, 3));
  const slotMat = new THREE.LineBasicMaterial({ color: 0xedd000, linewidth: 2 });
  const slotLine = new THREE.LineSegments(slotGeo, slotMat);
  slotLine.position.set(0, 0, 9);
  scene.add(slotLine);

  // Floating quote element projected 10 units directly above yellow car
  const commentEl = document.getElementById('car-frustrated-comment');
  function updateCommentText() {
    if (commentEl) {
      const idx = Math.floor(Math.random() * frustratedComments.length);
      commentEl.innerText = frustratedComments[idx];
    }
  }
  updateCommentText();
  setInterval(updateCommentText, 8000);

  const tempV = new THREE.Vector3();
  function updateCommentPosition() {
    if (!commentEl) return;

    // 3D position 10 units above main yellow car (x=0, y=10, z=9)
    tempV.set(mainCar.position.x, mainCar.position.y + 10, mainCar.position.z);
    tempV.project(camera);

    if (tempV.z > 1) {
      commentEl.style.display = 'none';
      return;
    }
    commentEl.style.display = 'block';

    const x = (tempV.x * 0.5 + 0.5) * container.clientWidth;
    const y = (tempV.y * -0.5 + 0.5) * container.clientHeight;

    commentEl.style.transform = `translate(-50%, -100%) translate(${x}px, ${y}px)`;
  }

  // Prewarm initial objects along the road
  spawners.forEach((s) => {
    for (let x = worldStart; x <= worldEnd; x += 110) {
      let obj;
      if (s.type === 'building') {
        obj = createBuildingSet(s.maxHeight);
        obj.position.set(x, 0.1, s.z);
        obj.userData = { speed: 30, z: s.z, type: 'building' };
      } else {
        obj = createCar(s.color);
        obj.position.set(x, 0.1, s.z);
        if ((s.speed || 30) < 0) {
          obj.rotation.y = Math.PI;
        }
        obj.userData = { speed: s.speed || 30, z: s.z, type: 'car' };
      }
      scene.add(obj);
      movingObjects.push(obj);
    }
  });

  const clock = new THREE.Clock();

  // Animation Loop
  function animate() {
    requestAnimationFrame(animate);
    const delta = clock.getDelta();

    // Move objects along the road
    for (let i = movingObjects.length - 1; i >= 0; i--) {
      const obj = movingObjects[i];
      obj.position.x += obj.userData.speed * delta;

      if (obj.userData.speed > 0 && obj.position.x > worldEnd + 50) {
        obj.position.x = worldStart;
      } else if (obj.userData.speed < 0 && obj.position.x < worldStart - 50) {
        obj.position.x = worldEnd;
      }
    }

    // Keep focus point locked on the yellow car
    controls.target.set(mainCar.position.x, mainCar.position.y + 0.3, mainCar.position.z);

    // Update floating frustrated comment position above yellow car
    updateCommentPosition();

    // Blinking effect for parking slot
    if (slotMat) {
      slotMat.opacity = 0.4 + 0.6 * Math.sin(clock.getElapsedTime() * 4);
      slotMat.transparent = true;
    }

    controls.update();
    renderer.render(scene, camera);
  }

  animate();

  // Responsive Canvas Resize
  window.addEventListener('resize', () => {
    if (!container || !canvas) return;
    const width = container.clientWidth;
    const height = container.clientHeight;
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
  });
});
