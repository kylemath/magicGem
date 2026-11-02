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
    this.precessionObjects = []; // Store objects for cleanup
    
    this.init();
  }
  
  init() {
    this.scene = new THREE.Scene();
    
    const aspect = this.container.clientWidth / this.container.clientHeight;
    this.camera = new THREE.PerspectiveCamera(60, aspect, 0.1, 1000);
    this.camera.position.set(3, 4, 5);
    this.camera.lookAt(0, 0, 0);
    
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    this.renderer.setClearColor(0x0a0a1a, 0);
    this.container.appendChild(this.renderer.domElement);
    
    this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    
    // Lighting
    this.scene.add(new THREE.AmbientLight(0x404040, 0.6));
    const light = new THREE.DirectionalLight(0xffffff, 0.8);
    light.position.set(5, 5, 5);
    this.scene.add(light);
    
    // Central B-field axis (pointing UP along Z)
    this.addBFieldAxis();
    
    // Grid helper in XY plane
    const gridHelper = new THREE.GridHelper(4, 8, 0x222244, 0x111133);
    gridHelper.rotation.x = Math.PI / 2; // Rotate to XY plane
    gridHelper.position.z = -2;
    this.scene.add(gridHelper);
    
    window.addEventListener('resize', () => this.onResize());
    this.animate();
  }
  
  addBFieldAxis() {
    // Central B-field arrow pointing UP (along +Z)
    const bArrow = new THREE.ArrowHelper(
      new THREE.Vector3(0, 0, 1),  // Direction: +Z (up)
      new THREE.Vector3(0, 0, -2), // Start below center
      4.5,                          // Length
      0xffd700,                     // Gold color
      0.25, 0.12
    );
    bArrow.name = 'bFieldArrow';
    this.scene.add(bArrow);
    
    // B-field label
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 128;
    canvas.height = 64;
    ctx.fillStyle = '#ffd700';
    ctx.font = 'bold 36px serif';
    ctx.fillText('B', 48, 44);
    
    const texture = new THREE.CanvasTexture(canvas);
    const material = new THREE.SpriteMaterial({ map: texture, transparent: true });
    const sprite = new THREE.Sprite(material);
    sprite.position.set(0.4, 0, 2.5);
    sprite.scale.set(0.6, 0.3, 1);
    sprite.name = 'bFieldLabel';
    this.scene.add(sprite);
    
    // Add circular ring to show precession plane
    const ringGeometry = new THREE.RingGeometry(1.8, 1.85, 64);
    const ringMaterial = new THREE.MeshBasicMaterial({ 
      color: 0xffd700, 
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.3
    });
    const ring = new THREE.Mesh(ringGeometry, ringMaterial);
    ring.position.z = 0;
    ring.name = 'precessionRing';
    this.scene.add(ring);
  }
  
  setSpinGem(spinGem) {
    this.spinGem = spinGem;
    // Initialize spins tilted from z-axis so precession is visible
    // Each spin starts with magnitude |s| but tilted 30 degrees from z
    this.spinVectors = spinGem.spins.map(s => {
      const mag = Math.abs(s);
      const sign = Math.sign(s) || 1;
      const tiltAngle = Math.PI / 6; // 30 degrees from z
      return {
        x: mag * Math.sin(tiltAngle) * sign,
        y: 0,
        z: mag * Math.cos(tiltAngle) * sign
      };
    });
    this.time = 0;
    this.energyHistory = [];
    this.updateVisualization();
  }
  
  updateVisualization() {
    // Clear existing precession objects
    for (let obj of this.precessionObjects) {
      this.scene.remove(obj);
      if (obj.geometry) obj.geometry.dispose();
      if (obj.material) obj.material.dispose();
    }
    this.precessionObjects = [];
    
    if (!this.spinGem) return;
    
    const gem = this.spinGem;
    const maxSpin = Math.max(...gem.spins.map(Math.abs), 0.5);
    
    // Compute total magnetization for central arrow
    let totalM = {x: 0, y: 0, z: 0};
    
    // Add atoms and spin arrows - ALL spinning around central Z axis
    for (let i = 0; i < gem.n; i++) {
      const pos = gem.positions[i];
      const spin = this.spinVectors[i];
      
      // Atom sphere
      const atomGeometry = new THREE.SphereGeometry(0.1, 24, 24);
      const atomMaterial = new THREE.MeshPhongMaterial({ 
        color: 0x00d4ff,
        emissive: 0x004466,
        emissiveIntensity: 0.3
      });
      const atomMesh = new THREE.Mesh(atomGeometry, atomMaterial);
      atomMesh.position.set(pos.x, pos.y, pos.z);
      this.scene.add(atomMesh);
      this.precessionObjects.push(atomMesh);
      
      // Spin arrow - drawn FROM the atom position
      const spinMag = Math.sqrt(spin.x**2 + spin.y**2 + spin.z**2);
      if (spinMag > 0.01) {
        const dir = new THREE.Vector3(spin.x, spin.y, spin.z).normalize();
        const arrowLength = spinMag / maxSpin * 0.8;
        
        // Color based on z-component (parallel to B)
        const zRatio = spin.z / spinMag;
        const color = new THREE.Color().setHSL(
          zRatio > 0 ? 0.0 : 0.6, // Red for up, blue for down
          0.9,
          0.5
        );
        
        const arrow = new THREE.ArrowHelper(
          dir, 
          new THREE.Vector3(pos.x, pos.y, pos.z),
          arrowLength,
          color,
          0.15, 0.08
        );
        this.scene.add(arrow);
        this.precessionObjects.push(arrow);
        
        // Add precession cone trace (small circle showing precession path)
        const perpMag = Math.sqrt(spin.x**2 + spin.y**2);
        if (perpMag > 0.05) {
          const coneRadius = perpMag / maxSpin * 0.4;
          const coneGeometry = new THREE.RingGeometry(coneRadius - 0.02, coneRadius, 32);
          const coneMaterial = new THREE.MeshBasicMaterial({
            color: color,
            side: THREE.DoubleSide,
            transparent: true,
            opacity: 0.25
          });
          const coneRing = new THREE.Mesh(coneGeometry, coneMaterial);
          coneRing.position.set(pos.x, pos.y, pos.z + spin.z / maxSpin * 0.4);
          this.scene.add(coneRing);
          this.precessionObjects.push(coneRing);
        }
      }
      
      totalM.x += spin.x;
      totalM.y += spin.y;
      totalM.z += spin.z;
    }
    
    // Central magnetization vector (shows collective precession)
    const mMag = Math.sqrt(totalM.x**2 + totalM.y**2 + totalM.z**2);
    if (mMag > 0.1) {
      const mDir = new THREE.Vector3(totalM.x, totalM.y, totalM.z).normalize();
      const mArrow = new THREE.ArrowHelper(
        mDir,
        new THREE.Vector3(0, 0, 0),
        mMag / gem.n * 1.5,
        0xff006e, // Magenta for total M
        0.2, 0.1
      );
      this.scene.add(mArrow);
      this.precessionObjects.push(mArrow);
    }
  }
  
  step(dt = 0.016) {
    if (!this.spinGem || !this.isPlaying) return;
    
    // B-field along Z (up)
    const B = {x: 0, y: 0, z: this.options.bFieldStrength};
    const gamma = this.options.gamma;
    
    // Precess each spin around central B-field: ds/dt = gamma * s × B
    // With B along z: dx/dt = gamma * sy * Bz, dy/dt = -gamma * sx * Bz, dz/dt = 0
    for (let i = 0; i < this.spinVectors.length; i++) {
      const s = this.spinVectors[i];
      
      // Cross product s × B where B = (0, 0, Bz)
      const cross = {
        x: gamma * s.y * B.z,       // sy * Bz - sz * 0
        y: -gamma * s.x * B.z,      // sz * 0 - sx * Bz
        z: 0                         // sx * 0 - sy * 0
      };
      
      s.x += cross.x * dt;
      s.y += cross.y * dt;
      // s.z stays constant (component parallel to B doesn't precess)
      
      // Renormalize to preserve spin magnitude
      const mag = Math.sqrt(s.x**2 + s.y**2 + s.z**2);
      const origMag = Math.abs(this.spinGem.spins[i]);
      if (mag > 0.001 && origMag > 0.001) {
        const scale = origMag / mag;
        s.x *= scale;
        s.y *= scale;
        s.z *= scale;
      }
    }
    
    // Compute current energy using full spin vectors projected onto original positions
    const projectedSpins = this.spinVectors.map((s, i) => {
      // Project spin onto original direction (z-axis in initial config)
      return s.z;
    });
    const tempGem = new SpinGem(this.spinGem.positions, projectedSpins);
    
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
      // Reset with initial tilt
      this.spinVectors = this.spinGem.spins.map(s => {
        const mag = Math.abs(s);
        const sign = Math.sign(s) || 1;
        const tiltAngle = Math.PI / 6;
        return {
          x: mag * Math.sin(tiltAngle) * sign,
          y: 0,
          z: mag * Math.cos(tiltAngle) * sign
        };
      });
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
    
    // Initialize with octahedron
    const gem = SpinGem.octahedron();
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

