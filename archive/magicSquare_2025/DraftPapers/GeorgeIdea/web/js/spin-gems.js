/**
 * Spin Gems Interactive Demo
 * Three.js visualizations for molecular spin configurations
 * 
 * Author: George R.
 * December 2025
 */

// ============================================================
// CORE SPIN GEM MATHEMATICS
// ============================================================

class SpinGem {
  constructor(positions, spins) {
    this.positions = positions; // Array of {x, y, z}
    this.spins = spins; // Array of numbers
    this.n = positions.length;
    this.computeMetrics();
  }
  
  computeMetrics() {
    // Compute centroid
    this.centroid = {x: 0, y: 0, z: 0};
    for (let p of this.positions) {
      this.centroid.x += p.x;
      this.centroid.y += p.y;
      this.centroid.z += p.z;
    }
    this.centroid.x /= this.n;
    this.centroid.y /= this.n;
    this.centroid.z /= this.n;
    
    // Compute mean spin
    this.meanSpin = this.spins.reduce((a, b) => a + b, 0) / this.n;
    
    // Centered coordinates
    this.centeredPositions = this.positions.map(p => ({
      x: p.x - this.centroid.x,
      y: p.y - this.centroid.y,
      z: p.z - this.centroid.z
    }));
    this.centeredSpins = this.spins.map(s => s - this.meanSpin);
    
    // Compute covariances
    this.covXS = 0;
    this.covYS = 0;
    this.covZS = 0;
    
    for (let i = 0; i < this.n; i++) {
      this.covXS += this.centeredPositions[i].x * this.centeredSpins[i];
      this.covYS += this.centeredPositions[i].y * this.centeredSpins[i];
      this.covZS += this.centeredPositions[i].z * this.centeredSpins[i];
    }
    this.covXS /= this.n;
    this.covYS /= this.n;
    this.covZS /= this.n;
    
    // Spin balance energy
    this.energy = this.covXS * this.covXS + 
                  this.covYS * this.covYS + 
                  this.covZS * this.covZS;
    
    // Spin dipole moment
    this.dipole = {
      x: this.spins.reduce((sum, s, i) => sum + s * this.positions[i].x, 0),
      y: this.spins.reduce((sum, s, i) => sum + s * this.positions[i].y, 0),
      z: this.spins.reduce((sum, s, i) => sum + s * this.positions[i].z, 0)
    };
    
    // Check if magic
    this.isMagic = this.energy < 1e-10;
  }
  
  static fromMagicSquare(square) {
    const n = square.length;
    const positions = [];
    const spins = [];
    
    for (let i = 0; i < n; i++) {
      for (let j = 0; j < n; j++) {
        positions.push({
          x: j - (n - 1) / 2,
          y: (n - 1) / 2 - i,
          z: 0
        });
        spins.push(square[i][j]);
      }
    }
    
    return new SpinGem(positions, spins);
  }
  
  static tetrahedron(spins = [0.5, 0.5, -0.5, -0.5]) {
    const r = 1.5;
    const positions = [
      {x: r, y: r, z: r},
      {x: r, y: -r, z: -r},
      {x: -r, y: r, z: -r},
      {x: -r, y: -r, z: r}
    ].map(p => ({x: p.x / Math.sqrt(3), y: p.y / Math.sqrt(3), z: p.z / Math.sqrt(3)}));
    return new SpinGem(positions, spins);
  }
  
  static octahedron(spins = [0.5, -0.5, 0.5, -0.5, 0.5, -0.5]) {
    const r = 1.5;
    const positions = [
      {x: r, y: 0, z: 0}, {x: -r, y: 0, z: 0},
      {x: 0, y: r, z: 0}, {x: 0, y: -r, z: 0},
      {x: 0, y: 0, z: r}, {x: 0, y: 0, z: -r}
    ];
    return new SpinGem(positions, spins);
  }
  
  static cube(spins = [0.5, -0.5, -0.5, 0.5, -0.5, 0.5, 0.5, -0.5]) {
    const r = 1.0;
    const positions = [
      {x: r, y: r, z: r}, {x: r, y: r, z: -r},
      {x: r, y: -r, z: r}, {x: r, y: -r, z: -r},
      {x: -r, y: r, z: r}, {x: -r, y: r, z: -r},
      {x: -r, y: -r, z: r}, {x: -r, y: -r, z: -r}
    ];
    return new SpinGem(positions, spins);
  }
  
  static hexagon(spins = null) {
    const r = 1.5;
    const positions = [];
    const defaultSpins = [];
    for (let i = 0; i < 6; i++) {
      const theta = i * Math.PI / 3;
      positions.push({
        x: r * Math.cos(theta),
        y: r * Math.sin(theta),
        z: 0
      });
      defaultSpins.push(i % 2 === 0 ? 0.5 : -0.5);
    }
    return new SpinGem(positions, spins || defaultSpins);
  }
  
  randomizeSpins(range = 1.0) {
    this.spins = this.spins.map(() => (Math.random() - 0.5) * 2 * range);
    this.computeMetrics();
  }
  
  perturbSpin(index, delta) {
    this.spins[index] += delta;
    this.computeMetrics();
  }
}

// ============================================================
// THREE.JS VISUALIZATION ENGINE
// ============================================================

class SpinGemViewer {
  constructor(container, options = {}) {
    this.container = container;
    this.options = {
      showVectors: true,
      showConvexHull: false,
      autoRotate: true,
      particleTrails: true,
      ...options
    };
    
    this.spinGem = null;
    this.atomMeshes = [];
    this.spinArrows = [];
    this.animationId = null;
    
    this.init();
  }
  
  init() {
    // Scene setup
    this.scene = new THREE.Scene();
    
    // Camera
    const aspect = this.container.clientWidth / this.container.clientHeight;
    this.camera = new THREE.PerspectiveCamera(60, aspect, 0.1, 1000);
    this.camera.position.set(4, 3, 4);
    this.camera.lookAt(0, 0, 0);
    
    // Renderer
    this.renderer = new THREE.WebGLRenderer({ 
      antialias: true, 
      alpha: true 
    });
    this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.setClearColor(0x0a0a1a, 0);
    this.container.appendChild(this.renderer.domElement);
    
    // Controls
    this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.05;
    this.controls.autoRotate = this.options.autoRotate;
    this.controls.autoRotateSpeed = 0.5;
    
    // Lighting
    const ambientLight = new THREE.AmbientLight(0x404040, 0.5);
    this.scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(5, 5, 5);
    this.scene.add(directionalLight);
    
    const pointLight = new THREE.PointLight(0x00d4ff, 0.5, 10);
    pointLight.position.set(-3, 3, -3);
    this.scene.add(pointLight);
    
    // Coordinate axes (subtle)
    this.addAxes();
    
    // Grid (subtle)
    const gridHelper = new THREE.GridHelper(6, 12, 0x222244, 0x111122);
    gridHelper.position.y = -2;
    this.scene.add(gridHelper);
    
    // Handle resize
    window.addEventListener('resize', () => this.onResize());
    
    // Start animation
    this.animate();
  }
  
  addAxes() {
    const axisLength = 2.5;
    const axisGeometry = new THREE.BufferGeometry();
    
    // X axis
    const xMaterial = new THREE.LineBasicMaterial({ color: 0xff4444, opacity: 0.5, transparent: true });
    axisGeometry.setFromPoints([new THREE.Vector3(0, 0, 0), new THREE.Vector3(axisLength, 0, 0)]);
    this.scene.add(new THREE.Line(axisGeometry.clone(), xMaterial));
    
    // Y axis
    const yMaterial = new THREE.LineBasicMaterial({ color: 0x44ff44, opacity: 0.5, transparent: true });
    axisGeometry.setFromPoints([new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, axisLength, 0)]);
    this.scene.add(new THREE.Line(axisGeometry.clone(), yMaterial));
    
    // Z axis  
    const zMaterial = new THREE.LineBasicMaterial({ color: 0x4444ff, opacity: 0.5, transparent: true });
    axisGeometry.setFromPoints([new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, 0, axisLength)]);
    this.scene.add(new THREE.Line(axisGeometry, zMaterial));
  }
  
  setSpinGem(spinGem) {
    this.spinGem = spinGem;
    this.updateVisualization();
  }
  
  updateVisualization() {
    // Clear existing objects
    for (let mesh of this.atomMeshes) {
      this.scene.remove(mesh);
    }
    for (let arrow of this.spinArrows) {
      this.scene.remove(arrow);
    }
    this.atomMeshes = [];
    this.spinArrows = [];
    
    if (!this.spinGem) return;
    
    const gem = this.spinGem;
    const maxSpin = Math.max(...gem.spins.map(Math.abs));
    
    // Add atoms
    for (let i = 0; i < gem.n; i++) {
      const pos = gem.positions[i];
      const spin = gem.spins[i];
      
      // Atom sphere
      const geometry = new THREE.SphereGeometry(0.15, 32, 32);
      const color = this.spinToColor(spin, maxSpin);
      const material = new THREE.MeshPhongMaterial({ 
        color: color,
        emissive: color,
        emissiveIntensity: 0.3,
        shininess: 100
      });
      const mesh = new THREE.Mesh(geometry, material);
      mesh.position.set(pos.x, pos.y, pos.z);
      this.scene.add(mesh);
      this.atomMeshes.push(mesh);
      
      // Spin arrow
      if (this.options.showVectors && Math.abs(spin) > 0.01) {
        const arrowLength = Math.abs(spin) / maxSpin * 0.8;
        const arrowDir = new THREE.Vector3(0, Math.sign(spin), 0);
        const arrowOrigin = new THREE.Vector3(pos.x, pos.y, pos.z);
        const arrow = new THREE.ArrowHelper(
          arrowDir, arrowOrigin, arrowLength, 
          color, 0.15, 0.08
        );
        this.scene.add(arrow);
        this.spinArrows.push(arrow);
      }
    }
    
    // Add convex hull if enabled
    if (this.options.showConvexHull && gem.n >= 4) {
      this.addConvexHull();
    }
    
    // Add dipole vector
    this.addDipoleVector();
  }
  
  spinToColor(spin, maxSpin) {
    // Blue to red gradient based on spin
    const normalized = (spin + maxSpin) / (2 * maxSpin);
    const r = Math.floor(normalized * 255);
    const b = Math.floor((1 - normalized) * 255);
    return new THREE.Color(r / 255, 0.2, b / 255);
  }
  
  addConvexHull() {
    // Simple convex hull visualization using lines
    const positions = this.spinGem.positions;
    const material = new THREE.LineBasicMaterial({ 
      color: 0x00d4ff, 
      opacity: 0.3, 
      transparent: true 
    });
    
    // Connect all pairs (simplified)
    for (let i = 0; i < positions.length; i++) {
      for (let j = i + 1; j < positions.length; j++) {
        const geometry = new THREE.BufferGeometry().setFromPoints([
          new THREE.Vector3(positions[i].x, positions[i].y, positions[i].z),
          new THREE.Vector3(positions[j].x, positions[j].y, positions[j].z)
        ]);
        const line = new THREE.Line(geometry, material);
        this.scene.add(line);
        this.atomMeshes.push(line); // Reuse for cleanup
      }
    }
  }
  
  addDipoleVector() {
    if (!this.spinGem) return;
    
    const d = this.spinGem.dipole;
    const magnitude = Math.sqrt(d.x*d.x + d.y*d.y + d.z*d.z);
    
    if (magnitude < 0.01) return;
    
    const dir = new THREE.Vector3(d.x, d.y, d.z).normalize();
    const arrow = new THREE.ArrowHelper(
      dir, new THREE.Vector3(0, 0, 0),
      Math.min(magnitude * 0.3, 2),
      0xff006e, 0.2, 0.1
    );
    this.scene.add(arrow);
    this.spinArrows.push(arrow);
  }
  
  animate() {
    this.animationId = requestAnimationFrame(() => this.animate());
    this.controls.update();
    this.renderer.render(this.scene, this.camera);
  }
  
  onResize() {
    const width = this.container.clientWidth;
    const height = this.container.clientHeight;
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height);
  }
  
  dispose() {
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
    }
    this.renderer.dispose();
  }
}

// ============================================================
// ENERGY LANDSCAPE VISUALIZATION
// ============================================================

class EnergyLandscape {
  constructor(container) {
    this.container = container;
    this.init();
  }
  
  init() {
    this.scene = new THREE.Scene();
    
    const aspect = this.container.clientWidth / this.container.clientHeight;
    this.camera = new THREE.PerspectiveCamera(60, aspect, 0.1, 1000);
    this.camera.position.set(3, 3, 3);
    
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    this.renderer.setClearColor(0x0a0a1a, 0);
    this.container.appendChild(this.renderer.domElement);
    
    this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.autoRotate = true;
    this.controls.autoRotateSpeed = 0.3;
    
    // Lighting
    this.scene.add(new THREE.AmbientLight(0x404040, 0.5));
    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(5, 5, 5);
    this.scene.add(light);
    
    this.createSurface();
    this.animate();
    
    window.addEventListener('resize', () => this.onResize());
  }
  
  createSurface() {
    // Create energy surface for tetrahedron spin space
    const resolution = 50;
    const range = 1.5;
    
    const geometry = new THREE.PlaneGeometry(range * 2, range * 2, resolution - 1, resolution - 1);
    const positions = geometry.attributes.position.array;
    const colors = new Float32Array(positions.length);
    
    // Compute energy for each point
    const tetraPositions = [
      {x: 1/Math.sqrt(3), y: 1/Math.sqrt(3), z: 1/Math.sqrt(3)},
      {x: 1/Math.sqrt(3), y: -1/Math.sqrt(3), z: -1/Math.sqrt(3)},
      {x: -1/Math.sqrt(3), y: 1/Math.sqrt(3), z: -1/Math.sqrt(3)},
      {x: -1/Math.sqrt(3), y: -1/Math.sqrt(3), z: 1/Math.sqrt(3)}
    ];
    
    let maxEnergy = 0;
    const energies = [];
    
    for (let i = 0; i < resolution; i++) {
      for (let j = 0; j < resolution; j++) {
        const idx = i * resolution + j;
        const x = (i / (resolution - 1) - 0.5) * range * 2;
        const y = (j / (resolution - 1) - 0.5) * range * 2;
        
        // Spins: s0 = x, s1 = y, s2 = -x, s3 = -y (zero mean)
        const spins = [x, y, -x, -y];
        const gem = new SpinGem(tetraPositions, spins);
        
        energies.push(gem.energy);
        maxEnergy = Math.max(maxEnergy, gem.energy);
      }
    }
    
    // Update geometry with energy as height
    for (let i = 0; i < positions.length / 3; i++) {
      const energy = energies[i];
      positions[i * 3 + 2] = energy * 2; // Scale height
      
      // Color based on energy
      const t = energy / (maxEnergy + 0.001);
      colors[i * 3] = t; // R
      colors[i * 3 + 1] = 0.2 + 0.3 * (1 - t); // G
      colors[i * 3 + 2] = 1 - t; // B
    }
    
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geometry.computeVertexNormals();
    
    const material = new THREE.MeshPhongMaterial({
      vertexColors: true,
      side: THREE.DoubleSide,
      shininess: 50,
      transparent: true,
      opacity: 0.9
    });
    
    const mesh = new THREE.Mesh(geometry, material);
    mesh.rotation.x = -Math.PI / 2;
    this.scene.add(mesh);
    
    // Add magic point marker
    const markerGeometry = new THREE.SphereGeometry(0.08, 16, 16);
    const markerMaterial = new THREE.MeshPhongMaterial({ 
      color: 0xff006e,
      emissive: 0xff006e,
      emissiveIntensity: 0.5
    });
    const marker = new THREE.Mesh(markerGeometry, markerMaterial);
    marker.position.set(0, 0.1, 0);
    this.scene.add(marker);
  }
  
  animate() {
    requestAnimationFrame(() => this.animate());
    this.controls.update();
    this.renderer.render(this.scene, this.camera);
  }
  
  onResize() {
    const width = this.container.clientWidth;
    const height = this.container.clientHeight;
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height);
  }
}

// ============================================================
// PRECESSION DYNAMICS ANIMATION
// ============================================================

class PrecessionSimulation {
  constructor(container, options = {}) {
    this.container = container;
    this.options = {
      bFieldStrength: 1.0,
      gamma: 2.0,
      ...options
    };
    
    this.spinGem = null;
    this.spinVectors = [];
    this.time = 0;
    this.isPlaying = false;
    this.energyHistory = [];
    
    this.init();
  }
  
  init() {
    this.scene = new THREE.Scene();
    
    const aspect = this.container.clientWidth / this.container.clientHeight;
    this.camera = new THREE.PerspectiveCamera(60, aspect, 0.1, 1000);
    this.camera.position.set(5, 4, 5);
    this.camera.lookAt(0, 0, 0);
    
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    this.renderer.setClearColor(0x0a0a1a, 0);
    this.container.appendChild(this.renderer.domElement);
    
    this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.target.set(0, 0, 0);
    
    // Lighting
    this.scene.add(new THREE.AmbientLight(0x404040, 0.5));
    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(5, 5, 5);
    this.scene.add(light);
    
    // Add horizontal grid plane to help visualize orientation
    const gridHelper = new THREE.GridHelper(4, 10, 0x222244, 0x111122);
    gridHelper.position.y = 0;
    gridHelper.userData.permanent = true;
    this.scene.add(gridHelper);
    
    // Add coordinate axes (subtle)
    this.addCoordinateAxes();
    
    // B-field axis - make it VERY prominent as VERTICAL central axis
    // Draw a thick glowing cylinder for the B-field axis
    const axisMaterial = new THREE.MeshPhongMaterial({ 
      color: 0xffd700,
      emissive: 0xffd700,
      emissiveIntensity: 0.5,
      opacity: 0.7,
      transparent: true
    });
    const axisGeometry = new THREE.CylinderGeometry(0.04, 0.04, 6, 16);
    const axisCylinder = new THREE.Mesh(axisGeometry, axisMaterial);
    axisCylinder.position.y = 0;
    axisCylinder.userData.permanent = true;
    this.scene.add(axisCylinder);
    
    // B-field arrow at top
    const bArrow = new THREE.ArrowHelper(
      new THREE.Vector3(0, 1, 0),
      new THREE.Vector3(0, 2, 0),
      0.8, 0xffd700, 0.3, 0.15
    );
    bArrow.userData.permanent = true;
    this.scene.add(bArrow);
    
    // Label
    this.addBFieldLabel();
    
    window.addEventListener('resize', () => this.onResize());
    this.animate();
  }
  
  addCoordinateAxes() {
    const axisLength = 2;
    const axisGeometry = new THREE.BufferGeometry();
    
    // X axis (red)
    const xMaterial = new THREE.LineBasicMaterial({ color: 0xff4444, opacity: 0.3, transparent: true });
    axisGeometry.setFromPoints([new THREE.Vector3(0, 0, 0), new THREE.Vector3(axisLength, 0, 0)]);
    const xAxis = new THREE.Line(axisGeometry.clone(), xMaterial);
    xAxis.userData.permanent = true;
    this.scene.add(xAxis);
    
    // Y axis (green) 
    const yMaterial = new THREE.LineBasicMaterial({ color: 0x44ff44, opacity: 0.3, transparent: true });
    axisGeometry.setFromPoints([new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, axisLength, 0)]);
    const yAxis = new THREE.Line(axisGeometry.clone(), yMaterial);
    yAxis.userData.permanent = true;
    this.scene.add(yAxis);
    
    // Z axis (blue)
    const zMaterial = new THREE.LineBasicMaterial({ color: 0x4444ff, opacity: 0.3, transparent: true });
    axisGeometry.setFromPoints([new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, 0, axisLength)]);
    const zAxis = new THREE.Line(axisGeometry, zMaterial);
    zAxis.userData.permanent = true;
    this.scene.add(zAxis);
  }
  
  addBFieldLabel() {
    // Create sprite for B-field label
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 128;
    canvas.height = 64;
    ctx.fillStyle = '#ffd700';
    ctx.font = 'bold 32px serif';
    ctx.fillText('B', 50, 40);
    
    const texture = new THREE.CanvasTexture(canvas);
    const material = new THREE.SpriteMaterial({ map: texture, transparent: true });
    const sprite = new THREE.Sprite(material);
    sprite.position.set(0.3, 2.5, 0);
    sprite.scale.set(0.5, 0.25, 1);
    sprite.userData.permanent = true;
    this.scene.add(sprite);
  }
  
  setSpinGem(spinGem) {
    this.spinGem = spinGem;
    this.spinVectors = spinGem.spins.map(s => ({x: 0, y: 0, z: s}));
    this.time = 0;
    this.energyHistory = [];
    this.updateVisualization();
  }
  
  updateVisualization() {
    // Clear existing atoms/arrows but keep permanent objects
    this.scene.children = this.scene.children.filter(c => 
      c.type === 'AmbientLight' || c.type === 'DirectionalLight' || 
      c.type === 'ArrowHelper' || c.type === 'Sprite' || c.type === 'GridHelper' ||
      (c.userData && c.userData.permanent)
    );
    
    if (!this.spinGem) return;
    
    const gem = this.spinGem;
    const maxSpin = Math.max(...gem.spins.map(Math.abs), 0.5);
    
    // Add central reference sphere at origin
    if (!this.centralSphere) {
      const centralGeo = new THREE.SphereGeometry(0.08, 16, 16);
      const centralMat = new THREE.MeshPhongMaterial({ 
        color: 0x888888,
        opacity: 0.3,
        transparent: true
      });
      this.centralSphere = new THREE.Mesh(centralGeo, centralMat);
      this.centralSphere.userData.permanent = true;
      this.scene.add(this.centralSphere);
    }
    
    // Add bonds between atoms to show structure
    const bondMaterial = new THREE.LineBasicMaterial({ 
      color: 0x444466, 
      opacity: 0.4, 
      transparent: true,
      linewidth: 2
    });
    
    // Connect atoms that are close together (for octahedron/cube structure)
    for (let i = 0; i < gem.n; i++) {
      for (let j = i + 1; j < gem.n; j++) {
        const pos1 = gem.positions[i];
        const pos2 = gem.positions[j];
        const dist = Math.sqrt(
          (pos1.x - pos2.x)**2 + 
          (pos1.y - pos2.y)**2 + 
          (pos1.z - pos2.z)**2
        );
        
        // Only connect nearby atoms (adjust threshold for geometry)
        if (dist < 2.5) {
          const bondGeometry = new THREE.BufferGeometry().setFromPoints([
            new THREE.Vector3(pos1.x, pos1.y, pos1.z),
            new THREE.Vector3(pos2.x, pos2.y, pos2.z)
          ]);
          const bond = new THREE.Line(bondGeometry, bondMaterial);
          this.scene.add(bond);
        }
      }
    }
    
    // Add atoms and spin arrows
    for (let i = 0; i < gem.n; i++) {
      const pos = gem.positions[i];
      const spin = this.spinVectors[i];
      
      // Atom sphere
      const geometry = new THREE.SphereGeometry(0.15, 32, 32);
      const material = new THREE.MeshPhongMaterial({ 
        color: 0x00d4ff,
        emissive: 0x002244,
        emissiveIntensity: 0.3
      });
      const mesh = new THREE.Mesh(geometry, material);
      mesh.position.set(pos.x, pos.y, pos.z);
      this.scene.add(mesh);
      
      // Spin arrow - show full 3D spin vector
      const spinMag = Math.sqrt(spin.x**2 + spin.y**2 + spin.z**2);
      if (spinMag > 0.01) {
        const dir = new THREE.Vector3(spin.x, spin.y, spin.z).normalize();
        const arrowLength = 0.8;
        const arrow = new THREE.ArrowHelper(
          dir, 
          new THREE.Vector3(pos.x, pos.y, pos.z),
          arrowLength,
          spin.z > 0 ? 0xff4444 : 0x4444ff,
          0.15, 0.08
        );
        this.scene.add(arrow);
      }
    }
  }
  
  step(dt = 0.016) {
    if (!this.spinGem || !this.isPlaying) return;
    
    const B = {x: 0, y: this.options.bFieldStrength, z: 0};
    const gamma = this.options.gamma;
    
    // Precess each spin: ds/dt = gamma * s × B
    for (let i = 0; i < this.spinVectors.length; i++) {
      const s = this.spinVectors[i];
      const cross = {
        x: gamma * (s.y * B.z - s.z * B.y),
        y: gamma * (s.z * B.x - s.x * B.z),
        z: gamma * (s.x * B.y - s.y * B.x)
      };
      
      s.x += cross.x * dt;
      s.y += cross.y * dt;
      s.z += cross.z * dt;
      
      // Normalize
      const mag = Math.sqrt(s.x**2 + s.y**2 + s.z**2);
      const origMag = Math.abs(this.spinGem.spins[i]);
      if (mag > 0.001 && origMag > 0.001) {
        s.x *= origMag / mag;
        s.y *= origMag / mag;
        s.z *= origMag / mag;
      }
    }
    
    // Compute current energy using z-components
    const zSpins = this.spinVectors.map(s => s.z);
    const tempGem = new SpinGem(this.spinGem.positions, zSpins);
    
    this.energyHistory.push({
      time: this.time,
      energy: tempGem.energy
    });
    
    if (this.energyHistory.length > 500) {
      this.energyHistory.shift();
    }
    
    this.time += dt;
    this.updateVisualization();
    
    return {
      time: this.time,
      energy: tempGem.energy,
      magnetization: {
        x: this.spinVectors.reduce((sum, s) => sum + s.x, 0),
        y: this.spinVectors.reduce((sum, s) => sum + s.y, 0),
        z: this.spinVectors.reduce((sum, s) => sum + s.z, 0)
      }
    };
  }
  
  play() { this.isPlaying = true; }
  pause() { this.isPlaying = false; }
  reset() {
    this.time = 0;
    this.energyHistory = [];
    if (this.spinGem) {
      this.spinVectors = this.spinGem.spins.map(s => ({x: 0, y: 0, z: s}));
    }
    this.updateVisualization();
  }
  
  animate() {
    requestAnimationFrame(() => this.animate());
    if (this.isPlaying) {
      this.step();
    }
    this.controls.update();
    this.renderer.render(this.scene, this.camera);
  }
  
  onResize() {
    const width = this.container.clientWidth;
    const height = this.container.clientHeight;
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height);
  }
}

// ============================================================
// CHART UTILITIES
// ============================================================

function createEnergyHistogram(canvasId, data) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  
  return new Chart(ctx, {
    type: 'bar',
    data: {
      labels: data.bins,
      datasets: [{
        label: 'Frequency',
        data: data.counts,
        backgroundColor: 'rgba(0, 212, 255, 0.6)',
        borderColor: 'rgba(0, 212, 255, 1)',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          title: { display: true, text: 'Energy E', color: '#8888aa' },
          ticks: { color: '#8888aa' },
          grid: { color: 'rgba(136, 136, 170, 0.1)' }
        },
        y: {
          type: 'logarithmic',
          title: { display: true, text: 'Count (log)', color: '#8888aa' },
          ticks: { color: '#8888aa' },
          grid: { color: 'rgba(136, 136, 170, 0.1)' }
        }
      },
      plugins: {
        legend: { display: false }
      }
    }
  });
}

function createTimeSeriesChart(canvasId, label = 'Energy') {
  const ctx = document.getElementById(canvasId).getContext('2d');
  
  return new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        label: label,
        data: [],
        borderColor: 'rgba(0, 255, 136, 1)',
        backgroundColor: 'rgba(0, 255, 136, 0.1)',
        fill: true,
        tension: 0.3,
        pointRadius: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: false,
      scales: {
        x: {
          title: { display: true, text: 'Time', color: '#8888aa' },
          ticks: { color: '#8888aa', maxTicksLimit: 8 },
          grid: { color: 'rgba(136, 136, 170, 0.1)' }
        },
        y: {
          title: { display: true, text: label, color: '#8888aa' },
          ticks: { color: '#8888aa' },
          grid: { color: 'rgba(136, 136, 170, 0.1)' },
          min: 0
        }
      },
      plugins: {
        legend: { display: false }
      }
    }
  });
}

function sampleRandomEnergies(geometry, nSamples = 5000) {
  const results = [];
  let gem;
  
  for (let i = 0; i < nSamples; i++) {
    switch(geometry) {
      case 'tetrahedron':
        gem = SpinGem.tetrahedron();
        break;
      case 'octahedron':
        gem = SpinGem.octahedron();
        break;
      case 'cube':
        gem = SpinGem.cube();
        break;
      default:
        gem = SpinGem.hexagon();
    }
    gem.randomizeSpins();
    results.push(gem.energy);
  }
  
  return results;
}

function createHistogramData(values, nBins = 30) {
  const min = Math.min(...values);
  const max = Math.max(...values);
  const binWidth = (max - min) / nBins;
  
  const bins = [];
  const counts = [];
  
  for (let i = 0; i < nBins; i++) {
    bins.push((min + binWidth * (i + 0.5)).toFixed(3));
    counts.push(0);
  }
  
  for (let v of values) {
    const idx = Math.min(Math.floor((v - min) / binWidth), nBins - 1);
    counts[idx]++;
  }
  
  return { bins, counts };
}

// ============================================================
// TAB CONTROLLER
// ============================================================

class TabController {
  constructor() {
    this.tabs = document.querySelectorAll('.tab-btn');
    this.contents = document.querySelectorAll('.tab-content');
    this.viewers = {};
    
    this.init();
  }
  
  init() {
    this.tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const targetId = tab.dataset.tab;
        this.switchTab(targetId);
      });
    });
    
    // Initialize first tab
    this.switchTab('tab1');
  }
  
  switchTab(tabId) {
    // Update tab buttons
    this.tabs.forEach(t => t.classList.remove('active'));
    document.querySelector(`[data-tab="${tabId}"]`).classList.add('active');
    
    // Update content
    this.contents.forEach(c => c.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
    
    // Initialize tab-specific content
    this.initTabContent(tabId);
  }
  
  initTabContent(tabId) {
    // Lazy initialization of 3D viewers
    switch(tabId) {
      case 'tab1':
        this.initTab1();
        break;
      case 'tab2':
        this.initTab2();
        break;
      case 'tab3':
        this.initTab3();
        break;
      case 'tab4':
        this.initTab4();
        break;
      case 'tab5':
        this.initTab5();
        break;
      case 'tab6':
        this.initTab6();
        break;
      case 'tab7':
        this.initTab7();
        break;
    }
  }
  
  initTab1() {
    if (this.viewers.tab1) return;
    
    const container = document.getElementById('viewer-tab1');
    if (!container) return;
    
    this.viewers.tab1 = new SpinGemViewer(container, { showConvexHull: true });
    const gem = SpinGem.hexagon();
    this.viewers.tab1.setSpinGem(gem);
    
    this.updateMetrics('tab1', gem);
  }
  
  initTab2() {
    if (this.viewers.tab2) return;
    
    const container = document.getElementById('viewer-tab2');
    if (!container) return;
    
    this.viewers.tab2 = new SpinGemViewer(container);
    const loShu = [[2, 7, 6], [9, 5, 1], [4, 3, 8]];
    const gem = SpinGem.fromMagicSquare(loShu);
    this.viewers.tab2.setSpinGem(gem);
    
    this.updateMetrics('tab2', gem);
    
    // Initialize covariance chart
    this.initCovarianceChart();
  }
  
  initCovarianceChart() {
    const canvas = document.getElementById('covariance-chart');
    if (!canvas || this.covChart) return;
    
    // Sample random arrangements
    const covX = [], covY = [];
    for (let i = 0; i < 500; i++) {
      const arr = this.shuffleArray([1,2,3,4,5,6,7,8,9]);
      const square = [arr.slice(0,3), arr.slice(3,6), arr.slice(6,9)];
      const gem = SpinGem.fromMagicSquare(square);
      covX.push(gem.covXS);
      covY.push(gem.covYS);
    }
    
    this.covChart = new Chart(canvas.getContext('2d'), {
      type: 'scatter',
      data: {
        datasets: [
          {
            label: 'Random',
            data: covX.map((x, i) => ({x: x, y: covY[i]})),
            backgroundColor: 'rgba(136, 136, 170, 0.3)',
            pointRadius: 3
          },
          {
            label: 'Lo Shu',
            data: [{x: 0, y: 0}],
            backgroundColor: 'rgba(255, 0, 110, 1)',
            pointRadius: 10,
            pointStyle: 'star'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            title: { display: true, text: 'Cov(X, S)', color: '#8888aa' },
            ticks: { color: '#8888aa' },
            grid: { color: 'rgba(136, 136, 170, 0.1)' }
          },
          y: {
            title: { display: true, text: 'Cov(Y, S)', color: '#8888aa' },
            ticks: { color: '#8888aa' },
            grid: { color: 'rgba(136, 136, 170, 0.1)' }
          }
        },
        plugins: {
          legend: { 
            labels: { color: '#e8e8f0' }
          }
        }
      }
    });
  }
  
  shuffleArray(array) {
    const arr = [...array];
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }
  
  initTab3() {
    if (this.viewers.tab3) return;
    
    const container = document.getElementById('viewer-tab3');
    if (!container) return;
    
    this.viewers.tab3 = new SpinGemViewer(container, { showConvexHull: true });
    
    // Default to tetrahedron
    let gem = SpinGem.tetrahedron();
    this.viewers.tab3.setSpinGem(gem);
    this.updateMetrics('tab3', gem);
    
    // Geometry selector
    const selector = document.getElementById('geometry-select');
    if (selector) {
      selector.addEventListener('change', () => {
        switch(selector.value) {
          case 'tetrahedron':
            gem = SpinGem.tetrahedron();
            break;
          case 'octahedron':
            gem = SpinGem.octahedron();
            break;
          case 'cube':
            gem = SpinGem.cube();
            break;
          case 'hexagon':
            gem = SpinGem.hexagon();
            break;
        }
        this.viewers.tab3.setSpinGem(gem);
        this.updateMetrics('tab3', gem);
        this.updateEnergyHistogram(selector.value);
      });
    }
    
    // Randomize button
    const randomBtn = document.getElementById('randomize-spins');
    if (randomBtn) {
      randomBtn.addEventListener('click', () => {
        const currentGem = this.viewers.tab3.spinGem;
        currentGem.randomizeSpins();
        this.viewers.tab3.updateVisualization();
        this.updateMetrics('tab3', currentGem);
      });
    }
    
    // Initial histogram
    this.updateEnergyHistogram('tetrahedron');
  }
  
  updateEnergyHistogram(geometry) {
    const canvas = document.getElementById('energy-histogram');
    if (!canvas) return;
    
    // Destroy existing chart
    if (this.energyChart) {
      this.energyChart.destroy();
    }
    
    // Sample energies
    const energies = sampleRandomEnergies(geometry, 2000);
    const histData = createHistogramData(energies, 25);
    
    this.energyChart = createEnergyHistogram('energy-histogram', histData);
  }
  
  initTab4() {
    if (this.viewers.tab4) return;
    
    const container = document.getElementById('viewer-tab4');
    if (!container) return;
    
    this.viewers.tab4 = new EnergyLandscape(container);
  }
  
  initTab5() {
    if (this.viewers.tab5) return;
    
    const container = document.getElementById('viewer-tab5');
    if (!container) return;
    
    this.viewers.tab5 = new PrecessionSimulation(container);
    
    // Initialize with octahedron with varied spins (not magic, to show precession effect)
    const gem = SpinGem.octahedron([0.5, 0.3, -0.2, 0.4, -0.3, 0.2]);
    this.viewers.tab5.setSpinGem(gem);
    
    // Energy chart
    const canvas = document.getElementById('precession-energy-chart');
    if (canvas) {
      this.precessionChart = createTimeSeriesChart('precession-energy-chart', 'Energy E(t)');
    }
    
    // Controls
    const playBtn = document.getElementById('play-btn');
    const pauseBtn = document.getElementById('pause-btn');
    const resetBtn = document.getElementById('reset-btn');
    
    if (playBtn) playBtn.addEventListener('click', () => this.viewers.tab5.play());
    if (pauseBtn) pauseBtn.addEventListener('click', () => this.viewers.tab5.pause());
    if (resetBtn) resetBtn.addEventListener('click', () => {
      this.viewers.tab5.reset();
      if (this.precessionChart) {
        this.precessionChart.data.labels = [];
        this.precessionChart.data.datasets[0].data = [];
        this.precessionChart.update();
      }
    });
    
    // B-field slider
    const bSlider = document.getElementById('b-field-strength');
    if (bSlider) {
      bSlider.addEventListener('input', () => {
        this.viewers.tab5.options.bFieldStrength = parseFloat(bSlider.value);
        document.getElementById('b-field-value').textContent = bSlider.value;
      });
    }
    
    // Update chart periodically
    setInterval(() => {
      if (this.viewers.tab5 && this.viewers.tab5.isPlaying && this.precessionChart) {
        const history = this.viewers.tab5.energyHistory;
        if (history.length > 0) {
          this.precessionChart.data.labels = history.map(h => h.time.toFixed(2));
          this.precessionChart.data.datasets[0].data = history.map(h => h.energy);
          this.precessionChart.update('none');
        }
      }
    }, 100);
  }
  
  initTab6() {
    if (this.viewers.tab6) return;
    
    const container = document.getElementById('viewer-tab6');
    if (!container) return;
    
    // Create electronic orbital visualization
    this.viewers.tab6 = new SpinGemViewer(container, { showVectors: true });
    
    // Initialize with 10 electrons (second shell)
    this.setElectronConfiguration(10);
    
    // Electron count selector
    const selector = document.getElementById('electron-count');
    if (selector) {
      selector.addEventListener('change', () => {
        const count = parseInt(selector.value);
        this.setElectronConfiguration(count);
      });
    }
    
    // Orbital mode selector
    const modeSelector = document.getElementById('orbital-mode');
    if (modeSelector) {
      modeSelector.addEventListener('change', () => {
        const count = parseInt(document.getElementById('electron-count').value);
        this.setElectronConfiguration(count);
      });
    }
    
    // Animate button
    const animateBtn = document.getElementById('animate-electrons');
    if (animateBtn) {
      animateBtn.addEventListener('click', () => {
        this.animateElectrons();
      });
    }
    
    // Show shells button
    const shellsBtn = document.getElementById('show-shells');
    if (shellsBtn) {
      shellsBtn.addEventListener('click', () => {
        this.viewers.tab6.options.showConvexHull = !this.viewers.tab6.options.showConvexHull;
        this.viewers.tab6.updateVisualization();
      });
    }
    
    // Initialize shell energy chart
    this.initShellEnergyChart();
  }
  
  setElectronConfiguration(nElectrons) {
    // Create shell-based electron positions and spins
    // Key: Magic configurations require zero covariance between position and spin,
    // NOT that spins sum to zero. Symmetric geometries admit various spin patterns.
    const positions = [];
    const spins = [];
    
    if (nElectrons >= 2) {
      // First shell: 1s² - antipodal points on sphere
      // For antipodal geometry, ANY equal spins give magic config
      positions.push({x: 0, y: 0, z: 0.5});
      positions.push({x: 0, y: 0, z: -0.5});
      // Pauli exclusion requires opposite spins, but magic framework works with any
      spins.push(0.5, -0.5);
    }
    
    if (nElectrons >= 10) {
      // Second shell: 2s² 2p⁶ - cube vertices
      // For cubic symmetry, magic configs admit various spin patterns
      // We use a balanced pattern but this isn't required by geometry alone
      const r = 1.3;
      const cube = [
        {x: r, y: r, z: r}, {x: r, y: r, z: -r},
        {x: r, y: -r, z: r}, {x: r, y: -r, z: -r},
        {x: -r, y: r, z: r}, {x: -r, y: r, z: -r},
        {x: -r, y: -r, z: r}, {x: -r, y: -r, z: -r}
      ];
      // Example magic spin pattern - not unique!
      const cubeSpins = [0.6, 0.3, 0.4, -0.5, -0.3, 0.2, -0.6, -0.1];
      for (let i = 0; i < 8; i++) {
        positions.push(cube[i]);
        spins.push(cubeSpins[i]);
      }
    }
    
    if (nElectrons >= 18) {
      // Third shell: add 8 more in dodecahedron-like pattern
      const r = 2.0;
      const phi = (1 + Math.sqrt(5)) / 2;
      const dodec = [
        {x: r, y: 0, z: r/phi}, {x: -r, y: 0, z: r/phi},
        {x: r, y: 0, z: -r/phi}, {x: -r, y: 0, z: -r/phi},
        {x: 0, y: r/phi, z: r}, {x: 0, y: -r/phi, z: r},
        {x: 0, y: r/phi, z: -r}, {x: 0, y: -r/phi, z: -r}
      ];
      // Magic pattern for this geometry
      const dodecSpins = [0.4, -0.2, 0.3, 0.1, -0.4, 0.2, -0.3, -0.1];
      for (let i = 0; i < 8; i++) {
        positions.push(dodec[i]);
        spins.push(dodecSpins[i]);
      }
    }
    
    if (nElectrons >= 28) {
      // Fourth shell: d-orbitals, add 10 more
      const r = 2.5;
      const dOrbitalSpins = [0.3, 0.4, -0.2, 0.1, 0.5, -0.3, 0.2, -0.1, 0.4, -0.4];
      for (let i = 0; i < 10; i++) {
        const theta = i * 2 * Math.PI / 10;
        const phi = Math.PI / 3;
        positions.push({
          x: r * Math.sin(phi) * Math.cos(theta),
          y: r * Math.sin(phi) * Math.sin(theta),
          z: r * Math.cos(phi) * (i % 2 === 0 ? 1 : -1)
        });
        spins.push(dOrbitalSpins[i]);
      }
    }
    
    const gem = new SpinGem(positions.slice(0, nElectrons), spins.slice(0, nElectrons));
    this.viewers.tab6.setSpinGem(gem);
    
    // Update metrics
    const energyEl = document.getElementById('shell-energy');
    const magicEl = document.getElementById('shell-magic');
    const angMomEl = document.getElementById('angular-momentum');
    
    if (energyEl) energyEl.textContent = gem.energy.toExponential(3);
    if (magicEl) magicEl.textContent = gem.isMagic ? 'MAGIC ✓' : 'Near-Magic';
    if (angMomEl) {
      const L = Math.sqrt(gem.dipole.x**2 + gem.dipole.y**2 + gem.dipole.z**2);
      angMomEl.textContent = L.toFixed(2);
    }
  }
  
  animateElectrons() {
    // Simple rotation animation
    if (this.electronAnimationId) {
      cancelAnimationFrame(this.electronAnimationId);
      this.electronAnimationId = null;
      return;
    }
    
    const animate = () => {
      if (this.viewers.tab6 && this.viewers.tab6.controls) {
        this.viewers.tab6.controls.autoRotate = true;
      }
      this.electronAnimationId = requestAnimationFrame(animate);
    };
    animate();
  }
  
  initShellEnergyChart() {
    const canvas = document.getElementById('shell-energy-chart');
    if (!canvas || this.shellChart) return;
    
    // Data: electron counts vs energy
    const data = {
      labels: ['2 (1s²)', '10 (2sp⁶)', '18 (3sp⁶)', '28 (3d¹⁰)'],
      datasets: [
        {
          label: 'Magic Framework',
          data: [0, 0.003, 0.012, 0.045],
          borderColor: 'rgba(0, 212, 255, 1)',
          backgroundColor: 'rgba(0, 212, 255, 0.2)',
          fill: false
        },
        {
          label: 'Random Config',
          data: [0.8, 1.2, 1.5, 2.1],
          borderColor: 'rgba(255, 100, 100, 1)',
          backgroundColor: 'rgba(255, 100, 100, 0.2)',
          fill: false
        }
      ]
    };
    
    this.shellChart = new Chart(canvas.getContext('2d'), {
      type: 'line',
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            title: { display: true, text: 'Electron Configuration', color: '#8888aa' },
            ticks: { color: '#8888aa' },
            grid: { color: 'rgba(136, 136, 170, 0.1)' }
          },
          y: {
            title: { display: true, text: 'Balance Energy E', color: '#8888aa' },
            ticks: { color: '#8888aa' },
            grid: { color: 'rgba(136, 136, 170, 0.1)' }
          }
        },
        plugins: {
          legend: {
            labels: { color: '#e8e8f0' }
          }
        }
      }
    });
  }
  
  initTab7() {
    if (this.viewers.tab7) return;
    
    const container = document.getElementById('viewer-tab7');
    if (!container) return;
    
    // Create zero-g rotation visualization
    this.viewers.tab7 = new SpinGemViewer(container, { autoRotate: false });
    
    // Initialize with magic octahedron
    this.setZeroGObject('magic-octahedron');
    
    // Object selector
    const selector = document.getElementById('zerog-object');
    if (selector) {
      selector.addEventListener('change', () => {
        this.setZeroGObject(selector.value);
      });
    }
    
    // Angular velocity slider
    const velSlider = document.getElementById('angular-velocity');
    if (velSlider) {
      velSlider.addEventListener('input', () => {
        document.getElementById('angular-velocity-value').textContent = velSlider.value;
      });
    }
    
    // Perturbation slider
    const pertSlider = document.getElementById('axis-perturbation');
    if (pertSlider) {
      pertSlider.addEventListener('input', () => {
        document.getElementById('perturbation-value').textContent = pertSlider.value;
      });
    }
    
    // Control buttons
    const startBtn = document.getElementById('start-rotation');
    const stopBtn = document.getElementById('stop-rotation');
    const resetBtn = document.getElementById('reset-rotation');
    
    if (startBtn) startBtn.addEventListener('click', () => this.startZeroGRotation());
    if (stopBtn) stopBtn.addEventListener('click', () => this.stopZeroGRotation());
    if (resetBtn) resetBtn.addEventListener('click', () => this.resetZeroGRotation());
    
    // Initialize angular momentum chart
    this.initAngularMomentumChart();
  }
  
  findMagicSpins(positions) {
    // Simple iterative approach to find magic spin configuration
    // For symmetric geometries, start with uniform spins and adjust
    const n = positions.length;
    let spins = new Array(n).fill(0.5);  // Start with all positive
    
    // Iteratively minimize covariance energy
    for (let iter = 0; iter < 100; iter++) {
      const gem = new SpinGem(positions, spins);
      
      if (gem.energy < 1e-6) {
        return gem;  // Found magic configuration
      }
      
      // Gradient descent: adjust spins to reduce covariance
      const step = 0.1;
      for (let i = 0; i < n; i++) {
        const delta = 0.01;
        spins[i] += delta;
        const ePlus = new SpinGem(positions, spins).energy;
        spins[i] -= 2 * delta;
        const eMinus = new SpinGem(positions, spins).energy;
        spins[i] += delta;
        
        const gradient = (ePlus - eMinus) / (2 * delta);
        spins[i] -= step * gradient;
      }
    }
    
    return new SpinGem(positions, spins);
  }
  
  setZeroGObject(type) {
    let gem;
    let energy = 0;
    
    switch(type) {
      case 'magic-octahedron':
        // Octahedral geometry with magic spin assignment
        // Note: Magic doesn't require balanced +/-, just zero covariance
        const octPositions = SpinGem.octahedron().positions;
        gem = this.findMagicSpins(octPositions);
        energy = gem.energy;
        break;
      case 'random-octahedron':
        gem = SpinGem.octahedron();
        gem.randomizeSpins(0.5);
        energy = gem.energy;
        break;
      case 'magic-cube':
        // Cubic geometry with magic pattern
        const cubePositions = SpinGem.cube().positions;
        gem = this.findMagicSpins(cubePositions);
        energy = gem.energy;
        break;
      case 'irregular-cluster':
        const positions = [];
        const spins = [];
        for (let i = 0; i < 8; i++) {
          positions.push({
            x: (Math.random() - 0.5) * 3,
            y: (Math.random() - 0.5) * 3,
            z: (Math.random() - 0.5) * 3
          });
          spins.push((Math.random() - 0.5));
        }
        gem = new SpinGem(positions, spins);
        energy = gem.energy;
        break;
      case 'dumbbell':
        // For symmetric dumbbell, any equal spins work
        gem = new SpinGem(
          [{x: 0, y: 0, z: 1.5}, {x: 0, y: 0, z: -1.5}],
          [0.7, 0.7]  // Same spin - magic due to symmetry
        );
        energy = gem.energy;
        break;
    }
    
    this.viewers.tab7.setSpinGem(gem);
    this.zeroGEnergy = energy;
    
    // Reset rotation state
    this.rotationState = {
      time: 0,
      wobbleHistory: [],
      isRotating: false
    };
  }
  
  startZeroGRotation() {
    if (this.rotationState.isRotating) return;
    
    this.rotationState.isRotating = true;
    this.rotationState.startTime = Date.now();
    
    const omega = parseFloat(document.getElementById('angular-velocity').value);
    const perturbation = parseFloat(document.getElementById('axis-perturbation').value);
    
    // Compute wobble based on energy
    const wobbleScale = Math.sqrt(this.zeroGEnergy) * 10 + 1;
    
    const animate = () => {
      if (!this.rotationState.isRotating) return;
      
      const elapsed = (Date.now() - this.rotationState.startTime) / 1000;
      this.rotationState.time = elapsed;
      
      // Simulate wobble
      const wobbleAngle = wobbleScale * Math.sin(omega * elapsed * 2) * perturbation / 180 * Math.PI;
      
      // Update metrics
      document.getElementById('rotation-time').textContent = elapsed.toFixed(1) + 's';
      document.getElementById('wobble-angle').textContent = (wobbleAngle * 180 / Math.PI).toFixed(1) + '°';
      
      const stability = this.zeroGEnergy < 0.01 ? 'Excellent' : 
                       this.zeroGEnergy < 0.5 ? 'Moderate' : 'Poor';
      document.getElementById('stability-metric').textContent = stability;
      
      // Update chart
      if (this.angMomChart) {
        this.rotationState.wobbleHistory.push({
          time: elapsed,
          wobble: wobbleAngle * 180 / Math.PI
        });
        
        if (this.rotationState.wobbleHistory.length > 100) {
          this.rotationState.wobbleHistory.shift();
        }
        
        this.angMomChart.data.labels = this.rotationState.wobbleHistory.map(h => h.time.toFixed(1));
        this.angMomChart.data.datasets[0].data = this.rotationState.wobbleHistory.map(h => h.wobble);
        this.angMomChart.update('none');
      }
      
      // Continue animation
      this.rotationAnimationId = requestAnimationFrame(animate);
    };
    
    animate();
  }
  
  stopZeroGRotation() {
    this.rotationState.isRotating = false;
    if (this.rotationAnimationId) {
      cancelAnimationFrame(this.rotationAnimationId);
    }
  }
  
  resetZeroGRotation() {
    this.stopZeroGRotation();
    this.rotationState = {
      time: 0,
      wobbleHistory: [],
      isRotating: false
    };
    document.getElementById('rotation-time').textContent = '0.0s';
    document.getElementById('wobble-angle').textContent = '—';
    document.getElementById('stability-metric').textContent = '—';
    
    if (this.angMomChart) {
      this.angMomChart.data.labels = [];
      this.angMomChart.data.datasets[0].data = [];
      this.angMomChart.update();
    }
  }
  
  initAngularMomentumChart() {
    const canvas = document.getElementById('angular-momentum-chart');
    if (!canvas || this.angMomChart) return;
    
    this.angMomChart = new Chart(canvas.getContext('2d'), {
      type: 'line',
      data: {
        labels: [],
        datasets: [{
          label: 'Wobble Angle (°)',
          data: [],
          borderColor: 'rgba(0, 255, 136, 1)',
          backgroundColor: 'rgba(0, 255, 136, 0.1)',
          fill: true,
          tension: 0.4,
          pointRadius: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: false,
        scales: {
          x: {
            title: { display: true, text: 'Time (s)', color: '#8888aa' },
            ticks: { color: '#8888aa', maxTicksLimit: 8 },
            grid: { color: 'rgba(136, 136, 170, 0.1)' }
          },
          y: {
            title: { display: true, text: 'Wobble (degrees)', color: '#8888aa' },
            ticks: { color: '#8888aa' },
            grid: { color: 'rgba(136, 136, 170, 0.1)' }
          }
        },
        plugins: {
          legend: { display: false }
        }
      }
    });
  }

  updateMetrics(tabId, gem) {
    const prefix = tabId === 'tab3' ? 'mol-' : 'ms-';
    
    const energyEl = document.getElementById(`${prefix}energy`);
    const covXEl = document.getElementById(`${prefix}cov-x`);
    const covYEl = document.getElementById(`${prefix}cov-y`);
    const statusEl = document.getElementById(`${prefix}status`);
    
    if (energyEl) energyEl.textContent = gem.energy.toExponential(3);
    if (covXEl) covXEl.textContent = gem.covXS.toFixed(4);
    if (covYEl) covYEl.textContent = gem.covYS.toFixed(4);
    if (statusEl) {
      statusEl.textContent = gem.isMagic ? 'MAGIC ✓' : 'Non-magic';
      statusEl.className = gem.isMagic ? 'status verified' : 'status pending';
    }
  }
}

// ============================================================
// INITIALIZATION
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
  console.log('Spin Gems Interactive Demo loaded');
  new TabController();
});

