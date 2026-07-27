// Single 3D Car Scene Background for Auth Screens (Login & Register)
window.addEventListener('DOMContentLoaded', () => {
  const canvas = document.getElementById('auth-scene-canvas-single');
  if (!canvas) return;
  const parent = canvas.parentElement;
  if (!parent) return;

  const scene = new THREE.Scene();
  const minFov = 30;
  const maxFov = 60;
  const radius = 100;
  const speed = 0.0015;

  const camera = new THREE.PerspectiveCamera(minFov, parent.clientWidth / parent.clientHeight, 0.1, 1000);
  camera.position.set(0, 200, 0);

  const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
  renderer.setSize(parent.clientWidth, parent.clientHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

  const ambientLight = new THREE.AmbientLight(0xffffff, 0.9);
  scene.add(ambientLight);
  const dirLight = new THREE.DirectionalLight(0xffffff, 0.6);
  dirLight.position.set(100, 200, 100);
  scene.add(dirLight);

  // Road
  const roadGeo = new THREE.PlaneGeometry(1000, 22);
  const roadMat = new THREE.MeshBasicMaterial({ color: 0x222222 });
  const road = new THREE.Mesh(roadGeo, roadMat);
  road.position.set(-120, -0.02, -0.5);
  road.rotation.x = -Math.PI / 2;
  scene.add(road);

  // Helper building set
  function createBuildingSet(maxHeight = 15) {
    const group = new THREE.Group();
    const numBuildings = 6;
    for (let i = 0; i < numBuildings; i++) {
      const floors = 2 + Math.floor(Math.random() * maxHeight);
      const width = 10 + Math.random() * 12;
      const length = 10 + Math.random() * 12;
      const height = floors * 4;

      const posX = (Math.random() - 0.5) * 40;
      const posZ = (Math.random() - 0.5) * 40;

      const geo = new THREE.BoxGeometry(width, height, length);
      const mat = new THREE.MeshBasicMaterial({ color: 0x333333, wireframe: true });
      const b = new THREE.Mesh(geo, mat);
      b.position.set(posX, height / 2, posZ);
      group.add(b);

      const roofGeo = new THREE.PlaneGeometry(width, length);
      const roofMat = new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.5 });
      const roof = new THREE.Mesh(roofGeo, roofMat);
      roof.position.set(posX, height, posZ);
      roof.rotation.x = -Math.PI / 2;
      group.add(roof);
    }
    return group;
  }

  // Car geometry
  function createCar(color = 0x888888) {
    const group = new THREE.Group();
    const geo = new THREE.BoxGeometry(4.4, 0.6, 2.1);
    const mat = new THREE.MeshBasicMaterial({ color: color });
    const carMesh = new THREE.Mesh(geo, mat);
    carMesh.position.y = 0.3;
    group.add(carMesh);
    return group;
  }

  const worldStart = -400;
  const worldEnd = 300;
  const movingObjects = [];

  const positions = [192, 72, -73, -193];
  positions.forEach((z) => {
    for (let x = worldStart; x <= worldEnd; x += 120) {
      const b = createBuildingSet(12);
      b.position.set(x, 0.1, z);
      b.userData = { speed: 30 };
      scene.add(b);
      movingObjects.push(b);
    }
  });

  const carLanes = [
    { z: -10, speed: 30, color: 0x666666 },
    { z: -2, speed: 32, color: 0x888888 },
    { z: 6, speed: -28, color: 0xedd000 },
    { z: 12, speed: 25, color: 0xaaaaaa }
  ];
  carLanes.forEach((lane) => {
    for (let x = worldStart; x <= worldEnd; x += 140) {
      const car = createCar(lane.color);
      car.position.set(x, 0.1, lane.z);
      if (lane.speed < 0) car.rotation.y = Math.PI;
      car.userData = { speed: lane.speed };
      scene.add(car);
      movingObjects.push(car);
    }
  });

  let angle = Math.random() * radius;
  const clock = new THREE.Clock();

  function animate() {
    requestAnimationFrame(animate);
    const delta = clock.getDelta();
    const time = clock.getElapsedTime();

    // Rotating Camera logic
    angle = (angle + speed) % (2 * Math.PI);
    camera.position.x = radius * Math.sin(angle);
    camera.position.z = radius * Math.cos(angle);
    camera.position.y = 140;
    camera.lookAt(1, 0, 1);

    const amplitude = (maxFov - minFov) / 2;
    camera.fov = minFov + amplitude + Math.sin(time * 0.05) * amplitude;
    camera.updateProjectionMatrix();

    // Move objects
    for (let i = movingObjects.length - 1; i >= 0; i--) {
      const obj = movingObjects[i];
      obj.position.x += obj.userData.speed * delta;
      if (obj.userData.speed > 0 && obj.position.x > worldEnd + 50) {
        obj.position.x = worldStart;
      } else if (obj.userData.speed < 0 && obj.position.x < worldStart - 50) {
        obj.position.x = worldEnd;
      }
    }

    renderer.render(scene, camera);
  }
  animate();

  window.addEventListener('resize', () => {
    if (!parent || !canvas) return;
    camera.aspect = parent.clientWidth / parent.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(parent.clientWidth, parent.clientHeight);
  });
});
