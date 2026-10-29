/**
 * The Hidden Mechanics of Magic Gems (Paper C) — Interactive Visual Essay Simulators (index.html)
 * Author: Kyle Elliott Mathewson, University of Alberta
 *
 * Implements 6 self-contained interactive physics labs:
 *   0. 2D-to-3D Magic Gem Lift Playground (#sim-intro)
 *   1. Three-Ring Radial Vector & Diophantine Pell Explorer (#sim-rings)
 *   2. Zero-Gravity 3D Euler Precession & Dzhanibekov Tennis-Racket Lab (#sim-precession)
 *   3. "Diamond-in-a-Diamond" Nested Core Inclusion & Fulcrum Pendulum Lab (#sim-nested)
 *   4. Wireframes, Complete K16 Strut Networks & Unfolded Papercraft Cutout Nets (#sim-fab)
 *   5. Mirror-Twin Tower Builder & Tilting-Table Toppling Simulator (#sim-stacking)
 */
(function () {
  "use strict";

  const GEMS = window.FEATURED_GEMS || {};
  const ALL880 = window.ALL880_SUMMARY || [];
  const ALL880_SQ = window.ALL880_SQUARES || [];

  // Grid cell coordinates for n=4: x_j = -1.5 + j, y_i = 1.5 - i
  const GRID_XY = [];
  for (let i = 0; i < 4; i++) {
    for (let j = 0; j < 4; j++) {
      const x = -1.5 + j;
      const y = 1.5 - i;
      const r2 = x * x + y * y;
      const r = Math.sqrt(r2);
      const ring = Math.abs(r2 - 0.5) < 0.01 ? 1 : (Math.abs(r2 - 2.5) < 0.01 ? 2 : 3);
      GRID_XY.push({ i, j, x, y, r, ux: x / r, uy: y / r, ring });
    }
  }

  const RING_RADII = {
    1: Math.SQRT2 / 2,         // 0.70710678
    2: Math.sqrt(10) / 2,      // 1.58113883
    3: (3 * Math.SQRT2) / 2    // 2.12132034
  };

  const RING_COLORS = {
    1: "#0f6b52", // Emerald inner ring
    2: "#2b5c8f", // Cobalt middle ring
    3: "#c85200"  // Amber/crimson outer ring
  };

  // =========================================================================
  // 3D Math & Projection Helpers
  // =========================================================================
  function vecAdd(a, b) { return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]; }
  function vecSub(a, b) { return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]; }
  function vecScale(a, s) { return [a[0] * s, a[1] * s, a[2] * s]; }
  function vecDot(a, b) { return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]; }
  function vecCross(a, b) {
    return [
      a[1] * b[2] - a[2] * b[1],
      a[2] * b[0] - a[0] * b[2],
      a[0] * b[1] - a[1] * b[0]
    ];
  }
  function vecNorm(a) { return Math.hypot(a[0], a[1], a[2]); }
  function vecNormalize(a) {
    const n = vecNorm(a);
    return n > 1e-12 ? [a[0] / n, a[1] / n, a[2] / n] : [0, 0, 1];
  }

  function matVec(M, v) {
    return [
      M[0][0] * v[0] + M[0][1] * v[1] + M[0][2] * v[2],
      M[1][0] * v[0] + M[1][1] * v[1] + M[1][2] * v[2],
      M[2][0] * v[0] + M[2][1] * v[1] + M[2][2] * v[2]
    ];
  }

  function matMul(A, B) {
    const C = [
      [0, 0, 0],
      [0, 0, 0],
      [0, 0, 0]
    ];
    for (let i = 0; i < 3; i++) {
      for (let j = 0; j < 3; j++) {
        C[i][j] = A[i][0] * B[0][j] + A[i][1] * B[1][j] + A[i][2] * B[2][j];
      }
    }
    return C;
  }

  function orthoNormalize3x3(R) {
    const c0 = vecNormalize([R[0][0], R[1][0], R[2][0]]);
    let c1 = [R[0][1], R[1][1], R[2][1]];
    const d01 = vecDot(c0, c1);
    c1 = vecNormalize(vecSub(c1, vecScale(c0, d01)));
    const c2 = vecCross(c0, c1);
    return [
      [c0[0], c1[0], c2[0]],
      [c0[1], c1[1], c2[1]],
      [c0[2], c1[2], c2[2]]
    ];
  }

  // Exact SO(3) exponential map exp([w * dt]_x) via Rodrigues' rotation formula
  function rodriguesExp(w, dt) {
    const wx = w[0] * dt, wy = w[1] * dt, wz = w[2] * dt;
    const theta = Math.hypot(wx, wy, wz);
    if (theta < 1e-12) {
      return [
        [1, -wz, wy],
        [wz, 1, -wx],
        [-wy, wx, 1]
      ];
    }
    const ux = wx / theta, uy = wy / theta, uz = wz / theta;
    const s = Math.sin(theta), c = 1 - Math.cos(theta);
    return [
      [1 - c * (uy * uy + uz * uz), -s * uz + c * ux * uy, s * uy + c * ux * uz],
      [s * uz + c * ux * uy, 1 - c * (ux * ux + uz * uz), -s * ux + c * uy * uz],
      [-s * uy + c * ux * uz, s * ux + c * uy * uz, 1 - c * (ux * ux + uy * uy)]
    ];
  }

  // Exact 3x3 symmetric Jacobi eigensolver returning sorted eigenvalues vals[0] <= vals[1] <= vals[2]
  // and right-handed orthonormal eigenvectors vecs = [e1, e2, e3]
  function jacobiEigen3x3(M) {
    const A = [
      [M[0][0], M[0][1], M[0][2]],
      [M[1][0], M[1][1], M[1][2]],
      [M[2][0], M[2][1], M[2][2]]
    ];
    const V = [
      [1, 0, 0],
      [0, 1, 0],
      [0, 0, 1]
    ];
    const pairs = [[0, 1], [0, 2], [1, 2]];
    for (let sweep = 0; sweep < 20; sweep++) {
      let off = Math.hypot(A[0][1], A[0][2], A[1][2]);
      if (off < 1e-14) break;
      for (let k = 0; k < 3; k++) {
        const p = pairs[k][0], q = pairs[k][1];
        const apq = A[p][q];
        if (Math.abs(apq) < 1e-15) continue;
        const diff = A[q][q] - A[p][p];
        let t;
        if (Math.abs(apq) < 1e-12 * Math.abs(diff)) {
          t = apq / diff;
        } else {
          const phi = diff / (2 * apq);
          t = 1 / (Math.abs(phi) + Math.sqrt(phi * phi + 1));
          if (phi < 0) t = -t;
        }
        const c = 1 / Math.sqrt(1 + t * t);
        const s = t * c;
        const tau = s / (1 + c);
        A[p][p] -= t * apq;
        A[q][q] += t * apq;
        A[p][q] = 0;
        A[q][p] = 0;
        for (let r = 0; r < 3; r++) {
          if (r !== p && r !== q) {
            const arp = A[r][p], arq = A[r][q];
            A[r][p] = arp - s * (arq + tau * arp);
            A[p][r] = A[r][p];
            A[r][q] = arq + s * (arp - tau * arq);
            A[q][r] = A[r][q];
          }
          const vrp = V[r][p], vrq = V[r][q];
          V[r][p] = vrp - s * (vrq + tau * vrp);
          V[r][q] = vrq + s * (vrp - tau * vrq);
        }
      }
    }
    const order = [0, 1, 2].sort(function (i, j) { return A[i][i] - A[j][j]; });
    const vals = order.map(function (i) { return A[i][i]; });
    function canonSign(v) {
      let m = 0;
      if (Math.abs(v[1]) > Math.abs(v[m])) m = 1;
      if (Math.abs(v[2]) > Math.abs(v[m])) m = 2;
      return v[m] < 0 ? [-v[0], -v[1], -v[2]] : v;
    }
    const e1 = canonSign(vecNormalize([V[0][order[0]], V[1][order[0]], V[2][order[0]]]));
    const e2 = canonSign(vecNormalize([V[0][order[1]], V[1][order[1]], V[2][order[1]]]));
    const e3 = vecCross(e1, e2);
    return { vals: vals, vecs: [e1, e2, e3] };
  }

  function project3D(pt, cam, width, height, scale) {
    // Camera orbit angles: yaw (azim around Z), pitch (elev)
    const cosY = Math.cos(cam.yaw);
    const sinY = Math.sin(cam.yaw);
    const cosP = Math.cos(cam.pitch);
    const sinP = Math.sin(cam.pitch);

    const x1 = pt[0] * cosY - pt[1] * sinY;
    const y1 = pt[0] * sinY + pt[1] * cosY;
    const z1 = pt[2];

    const xCam = x1;
    const yCam = z1 * cosP - y1 * sinP;
    const zDepth = z1 * sinP + y1 * cosP;

    const persp = 18 / (18 - zDepth * 0.35);
    return {
      x: width * 0.5 + xCam * scale * persp,
      y: height * 0.52 - yCam * scale * persp,
      depth: zDepth
    };
  }

  function attachOrbitControl(canvas, cam, onUpdate) {
    let dragging = false;
    let lastX = 0;
    let lastY = 0;
    canvas.style.cursor = "grab";
    canvas.addEventListener("mousedown", function (e) {
      dragging = true;
      lastX = e.clientX;
      lastY = e.clientY;
      canvas.style.cursor = "grabbing";
    });
    window.addEventListener("mousemove", function (e) {
      if (!dragging) return;
      const dx = e.clientX - lastX;
      const dy = e.clientY - lastY;
      lastX = e.clientX;
      lastY = e.clientY;
      cam.yaw += dx * 0.011;
      cam.pitch = Math.max(-1.25, Math.min(1.25, cam.pitch + dy * 0.011));
      if (onUpdate) onUpdate();
    });
    window.addEventListener("mouseup", function () {
      if (dragging) {
        dragging = false;
        canvas.style.cursor = "grab";
      }
    });
    canvas.addEventListener("touchstart", function (e) {
      if (e.touches && e.touches.length === 1) {
        dragging = true;
        lastX = e.touches[0].clientX;
        lastY = e.touches[0].clientY;
      }
    }, { passive: true });
    window.addEventListener("touchmove", function (e) {
      if (!dragging || !e.touches || e.touches.length !== 1) return;
      const dx = e.touches[0].clientX - lastX;
      const dy = e.touches[0].clientY - lastY;
      lastX = e.touches[0].clientX;
      lastY = e.touches[0].clientY;
      cam.yaw += dx * 0.011;
      cam.pitch = Math.max(-1.25, Math.min(1.25, cam.pitch + dy * 0.011));
      if (onUpdate) onUpdate();
    }, { passive: true });
    window.addEventListener("touchend", function () {
      dragging = false;
    });
  }

  function drawArrow2D(ctx, x0, y0, x1, y1, color, lineWidth, headSize) {
    const dx = x1 - x0;
    const dy = y1 - y0;
    const len = Math.hypot(dx, dy);
    if (len < 1e-3) return;
    const hs = headSize || 8;
    const angle = Math.atan2(dy, dx);
    ctx.save();
    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.lineWidth = lineWidth || 2;
    ctx.beginPath();
    ctx.moveTo(x0, y0);
    ctx.lineTo(x1, y1);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x1 - hs * Math.cos(angle - 0.42), y1 - hs * Math.sin(angle - 0.42));
    ctx.lineTo(x1 - hs * Math.cos(angle + 0.42), y1 - hs * Math.sin(angle + 0.42));
    ctx.closePath();
    ctx.fill();
    ctx.restore();
  }

  function getSquare4x4(idx0) {
    if (GEMS[String(idx0 + 1)] && GEMS[String(idx0 + 1)].S) {
      return GEMS[String(idx0 + 1)].S;
    }
    const flat = ALL880_SQ[idx0];
    if (!flat || flat.length !== 16) return null;
    return [
      flat.slice(0, 4),
      flat.slice(4, 8),
      flat.slice(8, 12),
      flat.slice(12, 16)
    ];
  }

  // Shared 4x4 "Square Lens" HUD overlay across Simulators 1–5
  function drawSquareLensHUD(ctx, S, opts) {
    if (!S || !opts || opts.show === false) return;
    const x0 = opts.x !== undefined ? opts.x : ctx.canvas.width - 118;
    const y0 = opts.y !== undefined ? opts.y : 30;
    const gap = 2;
    const pad = 6;
    const cellSz = opts.cellSz || (opts.size ? Math.max(17, Math.floor((opts.size - 2 * pad - 3 * gap) / 4)) : 21);
    const gridW = 4 * cellSz + 3 * gap;
    const boxW = gridW + 2 * pad;
    const boxH = gridW + 22 + pad;

    ctx.save();
    ctx.fillStyle = "rgba(255, 255, 255, 0.90)";
    ctx.strokeStyle = "rgba(19, 42, 44, 0.28)";
    ctx.lineWidth = 1.1;
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(x0, y0, boxW, boxH, 7);
    else ctx.rect(x0, y0, boxW, boxH);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = "#132a2c";
    ctx.font = "bold 9.5px -apple-system, BlinkMacSystemFont, sans-serif";
    ctx.textAlign = "left";
    ctx.textBaseline = "alphabetic";
    ctx.fillText(opts.title || "4×4 Lens", x0 + pad, y0 + 13);

    const innerSet = Object.assign({}, opts.innerSet || {});
    if (Array.isArray(opts.innerIdx)) {
      opts.innerIdx.forEach(function (vi) { innerSet[vi] = true; });
    }
    const topSet = Object.assign({}, opts.topSet || {});
    if (Array.isArray(opts.topVerts)) {
      opts.topVerts.forEach(function (vi) { topSet[vi] = true; });
    }
    const botSet = Object.assign({}, opts.botSet || {});
    if (Array.isArray(opts.botVerts)) {
      opts.botVerts.forEach(function (vi) { botSet[vi] = true; });
    }
    const hoverVerts = opts.hoverVerts || {};

    for (let i = 0; i < 4; i++) {
      for (let j = 0; j < 4; j++) {
        const k = i * 4 + j;
        const s = S[i][j];
        const z = s - 8.5;
        const cx = x0 + pad + j * (cellSz + gap);
        const cy = y0 + 18 + i * (cellSz + gap);
        let bg = "#f1f5f3";
        let fg = "#132a2c";
        let bdr = "rgba(19, 42, 44, 0.16)";
        let lw = 1.0;

        if (opts.mode === "rings") {
          const rIdx = GRID_XY[k].ring;
          bg = rIdx === 1 ? "rgba(15, 107, 82, 0.20)" : (rIdx === 2 ? "rgba(43, 92, 143, 0.20)" : "rgba(217, 130, 0, 0.22)");
          bdr = RING_COLORS[rIdx];
        } else if (opts.mode === "quadrupole") {
          const q = z * (-1.5 + j) * (1.5 - i);
          bg = q >= 0 ? "rgba(29, 78, 216, 0.18)" : "rgba(225, 29, 72, 0.18)";
          bdr = q >= 0 ? "rgba(29, 78, 216, 0.55)" : "rgba(225, 29, 72, 0.55)";
        } else if (opts.mode === "nested" || opts.mode === "hull") {
          const isIn = !!innerSet[k];
          bg = isIn ? "rgba(217, 119, 6, 0.25)" : "rgba(15, 118, 110, 0.17)";
          bdr = isIn ? "#d97706" : "rgba(15, 118, 110, 0.55)";
          if (isIn) lw = 1.6;
        } else if (opts.mode === "stacking") {
          if (topSet[k]) {
            bg = "rgba(15, 118, 110, 0.26)";
            bdr = "#0f766e";
            lw = 1.5;
          } else if (botSet[k]) {
            bg = "rgba(217, 119, 6, 0.26)";
            bdr = "#d97706";
            lw = 1.5;
          }
        }
        if (hoverVerts[k]) {
          bg = "#fef08a";
          bdr = "#dc2626";
          lw = 2.0;
        }

        ctx.fillStyle = bg;
        ctx.strokeStyle = bdr;
        ctx.lineWidth = lw;
        ctx.fillRect(cx, cy, cellSz, cellSz);
        ctx.strokeRect(cx, cy, cellSz, cellSz);

        ctx.fillStyle = fg;
        ctx.font = "bold 9.5px -apple-system, BlinkMacSystemFont, sans-serif";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(String(s), cx + cellSz * 0.5, cy + cellSz * 0.5 + 0.5);
      }
    }
    ctx.restore();
  }

  // =========================================================================
  // SIMULATOR 1: 3D & 2D Vectors from Origin O, Head-to-Tail Polygon & Pell Lab
  // =========================================================================
  function solve3x3(A, b) {
    // Gaussian elimination with partial pivoting for 3x3 system A * x = b
    const M = [
      [A[0][0], A[0][1], A[0][2], b[0]],
      [A[1][0], A[1][1], A[1][2], b[1]],
      [A[2][0], A[2][1], A[2][2], b[2]]
    ];
    for (let k = 0; k < 3; k++) {
      let maxRow = k;
      let maxVal = Math.abs(M[k][k]);
      for (let i = k + 1; i < 3; i++) {
        if (Math.abs(M[i][k]) > maxVal) {
          maxVal = Math.abs(M[i][k]);
          maxRow = i;
        }
      }
      if (maxVal < 1e-12) return [0, 0, 0];
      if (maxRow !== k) {
        const tmp = M[k];
        M[k] = M[maxRow];
        M[maxRow] = tmp;
      }
      for (let i = k + 1; i < 3; i++) {
        const f = M[i][k] / M[k][k];
        for (let j = k; j <= 3; j++) {
          M[i][j] -= f * M[k][j];
        }
      }
    }
    const x = [0, 0, 0];
    for (let i = 2; i >= 0; i--) {
      let s = M[i][3];
      for (let j = i + 1; j < 3; j++) s -= M[i][j] * x[j];
      x[i] = s / M[i][i];
    }
    return x;
  }

  function initSim1() {
    const viewModeSelect = document.getElementById("ring-view-mode");
    const sqSelect = document.getElementById("ring-sq-select");
    const alphaSlider = document.getElementById("ring-alpha-slider");
    const alphaVal = document.getElementById("ring-alpha-val");
    const btnAlpha0 = document.getElementById("btn-alpha-0");
    const btnAlpha1 = document.getElementById("btn-alpha-1");
    const btn3DWeights = document.getElementById("btn-3d-weights");
    const btnAlphaM1 = document.getElementById("btn-alpha-m1");
    const btnAlphaP3 = document.getElementById("btn-alpha-p3");
    const btnCollinear = document.getElementById("btn-collinear-tune");
    const btnLens = document.getElementById("btn-ring-lens");
    const canvasBoard = document.getElementById("canvas-ring-board");
    const canvasPell = document.getElementById("canvas-ring-pell");
    const readout = document.getElementById("ring-readout");
    if (!canvasBoard || !canvasPell) return;

    const ctxB = canvasBoard.getContext("2d");
    const ctxP = canvasPell.getContext("2d");

    let state = {
      viewMode: viewModeSelect ? viewModeSelect.value : "3d",
      sqKey: "70",
      customIdx0: null, // If user clicks any of the 880 points in the scatter plot
      alpha: 1.0,       // Power-law exponent alpha (2D) or beta (3D)
      weightedSphere: false,
      collinearCustomWeights: null, // If collinear tune is active: {l1, l2, l3}
      showLens: true,
      cam3D: { yaw: -0.68, pitch: 0.42 }
    };

    if (btnLens) {
      btnLens.addEventListener("click", function () {
        state.showLens = !state.showLens;
        btnLens.classList.toggle("active", state.showLens);
        renderSim1();
      });
    }

    attachOrbitControl(canvasBoard, state.cam3D, function () {
      if (state.viewMode === "3d") renderSim1();
    });

    function getDipoles() {
      const idx0 = state.customIdx0 !== null
        ? state.customIdx0
        : Math.max(0, Math.min(879, (parseInt(state.sqKey, 10) || 70) - 1));
      const row = ALL880[idx0] || [3, 0, 15, 0, 36, 6];
      const gem = GEMS[String(idx0 + 1)];
      return {
        idx1: idx0 + 1,
        label: "#" + (idx0 + 1) + " (Group " + row[5] + ")",
        din: [row[0], row[1]],
        dout: [row[2], row[3]],
        S: (gem && gem.S) ? gem.S : getSquare4x4(idx0)
      };
    }

    function evalResultant(din, dout, alpha, customW) {
      let l1, l2, l3;
      if (customW) {
        l1 = customW.l1;
        l2 = customW.l2;
        l3 = customW.l3;
      } else {
        l1 = Math.pow(RING_RADII[1], alpha);
        l2 = Math.pow(RING_RADII[2], alpha);
        l3 = Math.pow(RING_RADII[3], alpha);
      }
      const c1 = l1 / RING_RADII[1] - l2 / RING_RADII[2];
      const c3 = l3 / RING_RADII[3] - l2 / RING_RADII[2];
      const bx = c1 * din[0] + c3 * dout[0];
      const by = c1 * din[1] + c3 * dout[1];
      return { bx, by, norm: Math.hypot(bx, by), l1, l2, l3 };
    }

    function compute3DVectors(S, beta, useWeights) {
      if (!S) return { pts: [], V: [0, 0, 0], norm: 0, normScaled: 0, wStar: [], Rbar: 4.5 };
      const raw = [];
      let sumR = 0;
      const Phat = [];
      let V0 = [0, 0, 0];
      for (let k = 0; k < 16; k++) {
        const cell = GRID_XY[k];
        const sVal = S[cell.i][cell.j];
        const z = sVal - 8.5;
        const R = Math.hypot(cell.x, cell.y, z);
        sumR += R;
        const ph = [cell.x / R, cell.y / R, z / R];
        Phat.push(ph);
        V0[0] += ph[0];
        V0[1] += ph[1];
        V0[2] += ph[2];
        raw.push({ cell, sVal, z, R, ph });
      }
      const Rbar = sumR / 16.0;

      // Minimum-variance balancing weights w^* on unit sphere S^2:
      // w^* = 1 - Phat * (Phat^T * Phat)^{-1} * V0
      const G = [[0, 0, 0], [0, 0, 0], [0, 0, 0]];
      for (let k = 0; k < 16; k++) {
        for (let a = 0; a < 3; a++) {
          for (let b = 0; b < 3; b++) {
            G[a][b] += Phat[k][a] * Phat[k][b];
          }
        }
      }
      const lamVec = solve3x3(G, V0);
      const wStar = [];
      let wDiffSq = 0;
      let wMin = 999, wMax = -999;
      for (let k = 0; k < 16; k++) {
        const wk = 1.0 - (Phat[k][0] * lamVec[0] + Phat[k][1] * lamVec[1] + Phat[k][2] * lamVec[2]);
        wStar.push(wk);
        wDiffSq += (wk - 1.0) * (wk - 1.0);
        if (wk < wMin) wMin = wk;
        if (wk > wMax) wMax = wk;
      }

      let V = [0, 0, 0];
      const pts = raw.map(function (item, k) {
        const wk = useWeights ? wStar[k] : 1.0;
        const bExp = useWeights ? 0.0 : beta;
        const L = Math.pow(item.R, bExp);
        const vx = wk * L * item.ph[0];
        const vy = wk * L * item.ph[1];
        const vz = wk * L * item.ph[2];
        V[0] += vx;
        V[1] += vy;
        V[2] += vz;
        // For clean 3D viewport display across beta in [-1.2, 3.1], normalize visual length by Rbar^(beta-1)
        const visScale = useWeights ? 3.8 : (3.6 / Math.pow(Rbar, bExp));
        return {
          sVal: item.sVal,
          z: item.z,
          x: item.cell.x,
          y: item.cell.y,
          R: item.R,
          wk: wk,
          vx: vx,
          vy: vy,
          vz: vz,
          disp: [ item.ph[0] * L * visScale, item.ph[1] * L * visScale, item.ph[2] * L * visScale ]
        };
      });
      const norm = Math.hypot(V[0], V[1], V[2]);
      const normScaled = useWeights ? norm : norm / Math.pow(Rbar, beta - 1.0);
      return {
        pts: pts,
        V: V,
        V0: V0,
        norm: norm,
        normScaled: normScaled,
        wStar: wStar,
        wNormDiff: Math.sqrt(wDiffSq),
        wMin: wMin,
        wMax: wMax,
        Rbar: Rbar
      };
    }

    function updateActiveButtons() {
      const isTuned = state.collinearCustomWeights !== null;
      btnAlpha0.classList.toggle("active", !isTuned && !state.weightedSphere && Math.abs(state.alpha) < 1e-3);
      btnAlpha1.classList.toggle("active", !isTuned && !state.weightedSphere && Math.abs(state.alpha - 1.0) < 1e-3);
      if (btn3DWeights) btn3DWeights.classList.toggle("active", state.weightedSphere);
      if (btnAlphaM1) btnAlphaM1.classList.toggle("active", !isTuned && !state.weightedSphere && Math.abs(state.alpha + 1.0) < 1e-3);
      if (btnAlphaP3) btnAlphaP3.classList.toggle("active", !isTuned && !state.weightedSphere && Math.abs(state.alpha - 3.0) < 1e-3);
      btnCollinear.classList.toggle("active", isTuned);
      syncTabs();
    }

    function renderSim1() {
      const info = getDipoles();
      const din = info.din;
      const dout = info.dout;
      const dmid = [-(din[0] + dout[0]), -(din[1] + dout[1])];
      const uVec = [din[0] + dout[0] / 3, din[1] + dout[1] / 3];
      const vVec = [din[0] + dout[0], din[1] + dout[1]];
      const uNorm = Math.hypot(uVec[0], uVec[1]);
      const vNorm = Math.hypot(vVec[0], vVec[1]);
      const res = evalResultant(din, dout, state.alpha, state.collinearCustomWeights);
      const res3D = compute3DVectors(info.S, state.alpha, state.weightedSphere);

      const W = canvasBoard.width;
      const H = canvasBoard.height;
      ctxB.clearRect(0, 0, W, H);

      if (state.viewMode === "3d") {
        // ===================================================================
        // MODE 1: 3D Vectors from Origin O=(0,0,0) (Natural / Sphere S^2 / Power-Law beta)
        // ===================================================================
        const scale3D = 43.0;
        ctxB.fillStyle = "#132a2c";
        ctxB.font = "bold 12.5px -apple-system, BlinkMacSystemFont, sans-serif";
        const modeTitle = state.weightedSphere
          ? "3D Unit-Sphere Vectors p̂_ij with Balancing Weights w_ij* > 0 — " + info.label
          : (Math.abs(state.alpha) < 0.05
              ? "3D Unit Vectors p̂_ij on Sphere S² (β = 0) — " + info.label
              : "3D Origin Vectors L_ij = R_ij^β (β = " + state.alpha.toFixed(2) + ") — " + info.label);
        ctxB.fillText(modeTitle, 12, 20);

        // Draw 4x4 floor grid at z = 0
        ctxB.save();
        ctxB.strokeStyle = "rgba(120, 140, 132, 0.35)";
        ctxB.lineWidth = 1;
        for (let g = -1.5; g <= 1.51; g += 1.0) {
          const pA = project3D([-1.5, g, 0], state.cam3D, W, H, scale3D);
          const pB = project3D([1.5, g, 0], state.cam3D, W, H, scale3D);
          ctxB.beginPath(); ctxB.moveTo(pA.x, pA.y); ctxB.lineTo(pB.x, pB.y); ctxB.stroke();
          const pC = project3D([g, -1.5, 0], state.cam3D, W, H, scale3D);
          const pD = project3D([g, 1.5, 0], state.cam3D, W, H, scale3D);
          ctxB.beginPath(); ctxB.moveTo(pC.x, pC.y); ctxB.lineTo(pD.x, pD.y); ctxB.stroke();
        }
        ctxB.restore();

        // If near unit sphere (|beta| < 0.25 or weightedSphere), draw translucent sphere wireframe
        if (state.weightedSphere || Math.abs(state.alpha) < 0.25) {
          const rSph = state.weightedSphere ? 3.8 : 3.6;
          ctxB.save();
          ctxB.strokeStyle = "rgba(43, 92, 143, 0.22)";
          ctxB.lineWidth = 1.0;
          [-0.6, 0.0, 0.6].forEach(function (lat) {
            const zLat = rSph * Math.sin(lat);
            const rLat = rSph * Math.cos(lat);
            ctxB.beginPath();
            for (let s = 0; s <= 48; s++) {
              const ang = (s / 48) * Math.PI * 2;
              const pr = project3D([rLat * Math.cos(ang), rLat * Math.sin(ang), zLat], state.cam3D, W, H, scale3D);
              if (s === 0) ctxB.moveTo(pr.x, pr.y);
              else ctxB.lineTo(pr.x, pr.y);
            }
            ctxB.stroke();
          });
          [0, Math.PI / 2].forEach(function (lon) {
            ctxB.beginPath();
            for (let s = 0; s <= 48; s++) {
              const ang = (s / 48) * Math.PI * 2;
              const pr = project3D([
                rSph * Math.cos(ang) * Math.cos(lon),
                rSph * Math.cos(ang) * Math.sin(lon),
                rSph * Math.sin(ang)
              ], state.cam3D, W, H, scale3D);
              if (s === 0) ctxB.moveTo(pr.x, pr.y);
              else ctxB.lineTo(pr.x, pr.y);
            }
            ctxB.stroke();
          });
          ctxB.restore();
        }

        const pOrig = project3D([0, 0, 0], state.cam3D, W, H, scale3D);

        // Sort 16 3D vectors back-to-front by camera depth
        const sortedPts = res3D.pts.map(function (pt) {
          const pTip = project3D(pt.disp, state.cam3D, W, H, scale3D);
          const pFloor = project3D([pt.disp[0], pt.disp[1], 0], state.cam3D, W, H, scale3D);
          return { pt, pTip, pFloor, depth: pTip.depth };
        }).sort(function (a, b) { return a.depth - b.depth; });

        sortedPts.forEach(function (item) {
          const pt = item.pt;
          const col = pt.z > 0 ? "#D55E00" : "#0072B2"; // Okabe-Ito orange (z>0) and blue (z<0)
          // Dashed vertical drop line to z=0 plane
          ctxB.save();
          ctxB.strokeStyle = pt.z > 0 ? "rgba(213,94,0,0.24)" : "rgba(0,114,178,0.24)";
          ctxB.lineWidth = 1.0;
          ctxB.setLineDash([2, 2]);
          ctxB.beginPath();
          ctxB.moveTo(item.pFloor.x, item.pFloor.y);
          ctxB.lineTo(item.pTip.x, item.pTip.y);
          ctxB.stroke();
          ctxB.restore();

          // Vector arrow from origin O
          const lw = state.weightedSphere ? Math.max(1.2, 2.1 * pt.wk) : 2.1;
          drawArrow2D(ctxB, pOrig.x, pOrig.y, item.pTip.x, item.pTip.y, col, lw, 6.5);

          // Tip sphere (sized by w_ij^* in weighted-sphere mode)
          const rad = state.weightedSphere ? Math.max(2.6, 5.2 * Math.sqrt(Math.max(0.1, pt.wk))) : 3.6;
          ctxB.fillStyle = col;
          ctxB.strokeStyle = "#ffffff";
          ctxB.lineWidth = 1.0;
          ctxB.beginPath();
          ctxB.arc(item.pTip.x, item.pTip.y, rad, 0, Math.PI * 2);
          ctxB.fill();
          ctxB.stroke();

          // Entry label s_ij (and weight w_ij* if active)
          ctxB.fillStyle = "#182224";
          ctxB.font = "bold 10.5px -apple-system, sans-serif";
          const lbl = state.weightedSphere
            ? pt.sVal + " (" + pt.wk.toFixed(2) + ")"
            : String(pt.sVal);
          ctxB.fillText(lbl, item.pTip.x + 5, item.pTip.y - 4);
        });

        // Draw origin O marker
        ctxB.fillStyle = "#111111";
        ctxB.beginPath();
        ctxB.arc(pOrig.x, pOrig.y, 4.5, 0, Math.PI * 2);
        ctxB.fill();
        ctxB.fillText("O", pOrig.x - 13, pOrig.y + 4);

        // Draw 3D Resultant Vector V_beta (magnified when non-zero)
        if (res3D.normScaled > 1e-5) {
          const vScale = 2.6 / Math.pow(res3D.Rbar, state.weightedSphere ? 0 : (state.alpha - 1.0));
          const pRes = project3D([
            res3D.V[0] * vScale,
            res3D.V[1] * vScale,
            res3D.V[2] * vScale
          ], state.cam3D, W, H, scale3D);
          drawArrow2D(ctxB, pOrig.x, pOrig.y, pRes.x, pRes.y, "#CC0099", 3.8, 10);
          ctxB.fillStyle = "#CC0099";
          ctxB.font = "bold 11.5px -apple-system, sans-serif";
          ctxB.fillText("V_β", pRes.x + 6, pRes.y + 4);
        }

        // Bottom legend for 3D mode
        ctxB.font = "11.5px -apple-system, sans-serif";
        ctxB.fillStyle = "#D55E00";
        ctxB.fillText("● z_ij > 0 (entries 9..16)", 12, H - 25);
        ctxB.fillStyle = "#0072B2";
        ctxB.fillText("● z_ij < 0 (entries 1..8)", 170, H - 25);
        ctxB.fillStyle = "#0f6b52";
        ctxB.fillText(
          state.weightedSphere
            ? "w_ij* ∈ [" + res3D.wMin.toFixed(2) + ", " + res3D.wMax.toFixed(2) + "] (all > 0)"
            : (Math.abs(state.alpha - 3.0) < 0.05 ? "β=3 Cubic Law: (V_3)_z = 0 exact" : "Drag 3D canvas to orbit"),
          320, H - 25
        );
        ctxB.fillStyle = "#CC0099";
        ctxB.font = "bold 11.5px -apple-system, sans-serif";
        ctxB.fillText(
          "➔ 3D Resultant ||V||₂ = " + res3D.norm.toFixed(5) +
          "  (V_z = " + res3D.V[2].toFixed(4) + ")",
          12, H - 8
        );

      } else if (state.viewMode === "polygon") {
        // ===================================================================
        // MODE 2: 2D Radial Vectors from O & 16-Vector Head-to-Tail Polygon
        // ===================================================================
        ctxB.fillStyle = "#132a2c";
        ctxB.font = "bold 12.5px -apple-system, BlinkMacSystemFont, sans-serif";
        ctxB.fillText(
          "Left: 16 weighted arrows from O     |     Right: the same arrows head-to-tail",
          12, 20
        );

        // Compute the 16 2D vectors v_c = z_c * l(r_c) * u_c
        const S = info.S;
        const vecs2D = [];
        if (S) {
          GRID_XY.forEach(function (cell) {
            const sVal = S[cell.i][cell.j];
            const zVal = sVal - 8.5;
            const lRing = cell.ring === 1 ? res.l1 : (cell.ring === 2 ? res.l2 : res.l3);
            const vx = zVal * lRing * cell.ux;
            const vy = zVal * lRing * cell.uy;
            const ang = Math.atan2(vy, vx);
            vecs2D.push({ sVal, zVal, ring: cell.ring, vx, vy, ang });
          });
        }

        // Left sub-panel: Radial star from O1
        const cx1 = W * 0.25, cy1 = H * 0.52;
        let maxR = 1.0;
        vecs2D.forEach(function (v) {
          const m = Math.hypot(v.vx, v.vy);
          if (m > maxR) maxR = m;
        });
        const scStar = 92.0 / maxR;

        ctxB.strokeStyle = "#dfe5e1";
        ctxB.lineWidth = 1;
        ctxB.beginPath();
        ctxB.arc(cx1, cy1, 92, 0, Math.PI * 2);
        ctxB.stroke();

        vecs2D.forEach(function (v) {
          const col = RING_COLORS[v.ring];
          const tx = cx1 + v.vx * scStar;
          const ty = cy1 - v.vy * scStar;
          drawArrow2D(ctxB, cx1, cy1, tx, ty, col, 1.9, 5.5);
          ctxB.fillStyle = "#182224";
          ctxB.font = "10px -apple-system, sans-serif";
          ctxB.fillText(String(v.sVal), tx + (v.vx >= 0 ? 3 : -12), ty + (v.vy >= 0 ? -3 : 10));
        });
        ctxB.fillStyle = "#111";
        ctxB.beginPath(); ctxB.arc(cx1, cy1, 3.5, 0, Math.PI * 2); ctxB.fill();

        // Divider line
        ctxB.strokeStyle = "#e0e6e2";
        ctxB.beginPath(); ctxB.moveTo(W * 0.49, 30); ctxB.lineTo(W * 0.49, H - 38); ctxB.stroke();

        // Right sub-panel: 16-Vector Head-to-Tail Polygon sorted by direction angle
        const sortedPoly = vecs2D.slice().sort(function (a, b) { return a.ang - b.ang; });
        const chain = [[0, 0]];
        let curX = 0, curY = 0;
        sortedPoly.forEach(function (v) {
          curX += v.vx;
          curY += v.vy;
          chain.push([curX, curY]);
        });
        let minX = 0, maxX = 0, minY = 0, maxY = 0;
        chain.forEach(function (p) {
          if (p[0] < minX) minX = p[0];
          if (p[0] > maxX) maxX = p[0];
          if (p[1] < minY) minY = p[1];
          if (p[1] > maxY) maxY = p[1];
        });
        const span = Math.max(1e-3, Math.max(maxX - minX, maxY - minY));
        const scPoly = 195.0 / span;
        const cx2 = W * 0.74 - ((minX + maxX) * 0.5) * scPoly;
        const cy2 = H * 0.52 + ((minY + maxY) * 0.5) * scPoly;

        for (let k = 0; k < sortedPoly.length; k++) {
          const p0 = chain[k], p1 = chain[k + 1];
          const col = RING_COLORS[sortedPoly[k].ring];
          drawArrow2D(
            ctxB,
            cx2 + p0[0] * scPoly, cy2 - p0[1] * scPoly,
            cx2 + p1[0] * scPoly, cy2 - p1[1] * scPoly,
            col, 2.2, 5.5
          );
        }

        // Mark start O and final head
        const startX = cx2, startY = cy2;
        const endX = cx2 + curX * scPoly, endY = cy2 - curY * scPoly;
        ctxB.fillStyle = "#111";
        ctxB.beginPath(); ctxB.arc(startX, startY, 4.5, 0, Math.PI * 2); ctxB.fill();
        ctxB.font = "bold 11px -apple-system, sans-serif";
        ctxB.fillText("O (Start)", startX + 6, startY + 12);

        if (res.norm > 1e-4) {
          drawArrow2D(ctxB, startX, startY, endX, endY, "#CC0099", 3.4, 8.5);
          ctxB.fillStyle = "#CC0099";
          ctxB.fillText("Gap B", (startX + endX) * 0.5 + 6, (startY + endY) * 0.5 - 5);
          // Magnifier inset when the gap is too small to see (e.g. the 0.0705 Pell near-miss)
          if (res.norm * scPoly < 14) {
            const ix = W - 70, iy = 72, ir = 38;
            const gx = curX / res.norm, gy = curY / res.norm;
            const zoomRel = (ir * 0.62 / res.norm) / scPoly;
            ctxB.save();
            ctxB.fillStyle = "rgba(255,255,255,0.96)";
            ctxB.strokeStyle = "#CC0099";
            ctxB.lineWidth = 1.6;
            ctxB.beginPath(); ctxB.arc(ix, iy, ir, 0, Math.PI * 2); ctxB.fill(); ctxB.stroke();
            ctxB.beginPath(); ctxB.moveTo(endX, endY); ctxB.lineTo(ix - ir * 0.7, iy + ir * 0.7); ctxB.stroke();
            const sx = ix - gx * ir * 0.31, sy = iy + gy * ir * 0.31;
            ctxB.fillStyle = "#111";
            ctxB.beginPath(); ctxB.arc(sx, sy, 3, 0, Math.PI * 2); ctxB.fill();
            drawArrow2D(ctxB, sx, sy, ix + gx * ir * 0.31, iy - gy * ir * 0.31, "#CC0099", 2.4, 7);
            ctxB.fillStyle = "#CC0099";
            ctxB.font = "bold 10px -apple-system, sans-serif";
            ctxB.textAlign = "center";
            ctxB.fillText("zoom ×" + Math.round(zoomRel), ix, iy + ir + 13);
            ctxB.fillText("gap " + res.norm.toFixed(4), ix, iy + ir + 25);
            ctxB.restore();
          }
        } else {
          ctxB.fillStyle = "#0f6b52";
          ctxB.fillText("✓ Exact Closed 16-Gon on O", W * 0.55, H - 44);
        }

        // Bottom legend
        ctxB.font = "11.5px -apple-system, sans-serif";
        ctxB.fillStyle = RING_COLORS[1];
        ctxB.fillText("● R_in (r₁=√2/2)", 14, H - 24);
        ctxB.fillStyle = RING_COLORS[2];
        ctxB.fillText("● R_mid (r₂=√10/2)", 135, H - 24);
        ctxB.fillStyle = RING_COLORS[3];
        ctxB.fillText("● R_out (r₃=3√2/2)", 275, H - 24);
        ctxB.fillStyle = res.norm < 1e-4 ? "#0f6b52" : "#CC0099";
        ctxB.font = "bold 11.5px -apple-system, sans-serif";
        ctxB.fillText(
          "➔ Polygon Closure Gap ||B_{z,ℓ}(S)||₂ = " + res.norm.toFixed(6) +
          (res.norm < 1e-4 ? " (CLOSED)" : " (OPEN)"),
          14, H - 8
        );

      } else {
        // ===================================================================
        // MODE 3: 4x4 Grid, Three Concentric Rings & Ring Dipoles
        // ===================================================================
        const cx = W * 0.48;
        const cy = H * 0.52;
        const scale = 78;

        ctxB.fillStyle = "#132a2c";
        ctxB.font = "bold 13px -apple-system, BlinkMacSystemFont, sans-serif";
        ctxB.fillText("Three Concentric Rings & Radial Force Vectors — Square " + info.label, 14, 22);

        [1, 2, 3].forEach(function (rk) {
          ctxB.save();
          ctxB.strokeStyle = RING_COLORS[rk];
          ctxB.lineWidth = 1.4;
          ctxB.setLineDash([4, 4]);
          ctxB.beginPath();
          ctxB.arc(cx, cy, RING_RADII[rk] * scale, 0, Math.PI * 2);
          ctxB.stroke();
          ctxB.restore();
        });

        const S = info.S;
        GRID_XY.forEach(function (cell) {
          const px = cx + cell.x * scale;
          const py = cy - cell.y * scale;
          const col = RING_COLORS[cell.ring];

          ctxB.strokeStyle = "#dfe5e1";
          ctxB.lineWidth = 1;
          ctxB.strokeRect(px - scale * 0.48, py - scale * 0.48, scale * 0.96, scale * 0.96);

          if (S) {
            const sVal = S[cell.i][cell.j];
            const zVal = sVal - 8.5;
            const lRing = cell.ring === 1 ? res.l1 : (cell.ring === 2 ? res.l2 : res.l3);
            const vLen = zVal * lRing * 2.8;
            drawArrow2D(ctxB, px, py, px + cell.ux * vLen, py - cell.uy * vLen, col, 1.6, 5);
            ctxB.fillStyle = "#182224";
            ctxB.font = "bold 11px -apple-system, sans-serif";
            ctxB.fillText(String(sVal), px - 6, py - 8);
          }

          ctxB.fillStyle = col;
          ctxB.beginPath();
          ctxB.arc(px, py, 3.5, 0, Math.PI * 2);
          ctxB.fill();
        });

        const dipScale = 3.2;
        drawArrow2D(ctxB, cx, cy, cx + din[0] * dipScale, cy - din[1] * dipScale, RING_COLORS[1], 3.0, 8);
        drawArrow2D(ctxB, cx, cy, cx + dmid[0] * dipScale, cy - dmid[1] * dipScale, RING_COLORS[2], 3.0, 8);
        drawArrow2D(ctxB, cx, cy, cx + dout[0] * dipScale, cy - dout[1] * dipScale, RING_COLORS[3], 3.0, 8);

        const resScale = 16.0;
        drawArrow2D(ctxB, cx, cy, cx + res.bx * resScale, cy - res.by * resScale, "#d91b42", 3.6, 10);

        ctxB.font = "11.5px -apple-system, sans-serif";
        ctxB.fillStyle = RING_COLORS[1];
        ctxB.fillText("● R_in (r₁=√2/2): d_in=(" + din[0] + "," + din[1] + ")", 14, H - 26);
        ctxB.fillStyle = RING_COLORS[2];
        ctxB.fillText("● R_mid (r₂=√10/2): d_mid=(" + dmid[0] + "," + dmid[1] + ")", 195, H - 26);
        ctxB.fillStyle = RING_COLORS[3];
        ctxB.fillText("● R_out (r₃=3√2/2): d_out=(" + dout[0] + "," + dout[1] + ")", 14, H - 9);
        ctxB.fillStyle = "#d91b42";
        ctxB.font = "bold 11.5px -apple-system, sans-serif";
        ctxB.fillText("➔ Net Resultant ||B||₂ = " + res.norm.toFixed(6), 235, H - 9);
      }

      if (state.showLens && info.S) {
        drawSquareLensHUD(ctxB, info.S, {
          show: true,
          mode: "rings",
          title: "Square #" + info.idx1 + " (Rings)",
          x: W - 114,
          y: 28,
          cellSz: 21
        });
      }

      // ----- Right Canvas: Top = Power-Law Curve (3D or 2D), Bottom = 880 Pell Scatter -----
      const WP = canvasPell.width;
      const HP = canvasPell.height;
      ctxP.clearRect(0, 0, WP, HP);

      const padL = 48, padR = 20, topY = 30, topH = 145;
      ctxP.fillStyle = "#132a2c";
      ctxP.font = "bold 12px -apple-system, sans-serif";
      const is3D = state.viewMode === "3d";
      ctxP.fillText(
        is3D
          ? "3D Power-Law Profile ||V_β(S)||₂ / R̄^(β-1) vs. β (β ∈ [-1.2, 3.1])"
          : "2D Power-Law Profile ||B_{z,r^α}(S)||₂ vs. Exponent α (α ∈ [-1.2, 3.1])",
        14, 19
      );

      ctxP.strokeStyle = "#cbd5d0";
      ctxP.lineWidth = 1;
      ctxP.strokeRect(padL, topY, WP - padL - padR, topH);

      const aMin = -1.2, aMax = 3.1;
      const samples = [];
      let maxNorm = is3D ? 12.0 : 10.0;
      for (let k = 0; k <= 120; k++) {
        const a = aMin + ((aMax - aMin) * k) / 120;
        const r = is3D
          ? compute3DVectors(info.S, a, false).normScaled
          : evalResultant(din, dout, a, null).norm;
        samples.push({ a, r });
        if (r > maxNorm) maxNorm = r;
      }
      maxNorm = Math.min(maxNorm, 35.0);

      function xOfAlpha(a) {
        return padL + ((a - aMin) / (aMax - aMin)) * (WP - padL - padR);
      }
      function yOfNorm(n) {
        return topY + topH - Math.min(1, n / (maxNorm * 1.05)) * (topH - 14);
      }

      // Vertical reference lines at -1, 0, 1, 3
      [-1, 0, 1, 3].forEach(function (aRef) {
        const xx = xOfAlpha(aRef);
        ctxP.save();
        ctxP.strokeStyle = aRef === 1 ? "#0f6b52" : (aRef === 0 ? "#995800" : "#7b8a84");
        ctxP.setLineDash([3, 3]);
        ctxP.beginPath();
        ctxP.moveTo(xx, topY);
        ctxP.lineTo(xx, topY + topH);
        ctxP.stroke();
        ctxP.restore();
        ctxP.fillStyle = aRef === 1 ? "#0f6b52" : (aRef === 0 ? "#995800" : "#52605b");
        ctxP.font = "10px -apple-system, sans-serif";
        const sym = is3D ? "β=" : "α=";
        ctxP.fillText(sym + aRef, xx - 12, topY + 12);
      });

      ctxP.strokeStyle = is3D ? "#0072B2" : "#0f6b52";
      ctxP.lineWidth = 2.3;
      ctxP.beginPath();
      samples.forEach(function (pt, idx) {
        const xx = xOfAlpha(pt.a);
        const yy = yOfNorm(pt.r);
        if (idx === 0) ctxP.moveTo(xx, yy);
        else ctxP.lineTo(xx, yy);
      });
      ctxP.stroke();

      // Current marker on the power-law curve
      const aMark = state.weightedSphere ? 0.0 : state.alpha;
      const curX = xOfAlpha(aMark);
      const curveVal = is3D
        ? compute3DVectors(info.S, aMark, false).normScaled
        : evalResultant(din, dout, aMark, null).norm;
      const curveY = yOfNorm(curveVal);
      ctxP.fillStyle = "#CC0099";
      ctxP.beginPath();
      ctxP.arc(curX, curveY, 5.0, 0, Math.PI * 2);
      ctxP.fill();

      // If weightedSphere (in 3D) or collinearCustomWeights (in 2D) reduces resultant to 0 off the power-law curve, show drop arrow to 0
      if ((is3D && state.weightedSphere) || (!is3D && state.collinearCustomWeights !== null)) {
        const zeroY = yOfNorm(0.0);
        if (Math.abs(zeroY - curveY) > 3) {
          drawArrow2D(ctxP, curX, curveY + 3, curX, zeroY - 3, "#d98200", 1.8, 6);
        }
        ctxP.fillStyle = "#0f6b52";
        ctxP.strokeStyle = "#ffffff";
        ctxP.lineWidth = 1.2;
        ctxP.beginPath();
        ctxP.arc(curX, zeroY, 5.5, 0, Math.PI * 2);
        ctxP.fill();
        ctxP.stroke();
        ctxP.fillStyle = "#0f6b52";
        ctxP.font = "bold 10px -apple-system, sans-serif";
        ctxP.fillText(is3D ? "w* → 0" : "Tuned → 0", curX + 7, zeroY - 3);
      }

      // Bottom sub-panel: All 880 Magic Squares in (||u||, ||v||) Diophantine Pell Plane
      const botY = 212, botH = 195;
      ctxP.fillStyle = "#132a2c";
      ctxP.font = "bold 12.5px -apple-system, sans-serif";
      ctxP.fillText("All 880 Magic Squares in (||u||, ||v||) Plane vs. Irrational Ray v = √5 u", 14, 198);

      ctxP.strokeStyle = "#cbd5d0";
      ctxP.lineWidth = 1;
      ctxP.strokeRect(padL, botY, WP - padL - padR, botH);

      const maxU = 15.5;
      const maxV = 35.0;
      function xOfU(u) { return padL + (u / maxU) * (WP - padL - padR); }
      function yOfV(v) { return botY + botH - (v / maxV) * (botH - 10); }

      ctxP.save();
      ctxP.strokeStyle = "#d91b42";
      ctxP.lineWidth = 1.8;
      ctxP.setLineDash([5, 4]);
      ctxP.beginPath();
      ctxP.moveTo(xOfU(0), yOfV(0));
      ctxP.lineTo(xOfU(maxU), yOfV(maxU * Math.sqrt(5)));
      ctxP.stroke();
      ctxP.restore();
      ctxP.fillStyle = "#d91b42";
      ctxP.font = "bold 11px -apple-system, sans-serif";
      ctxP.fillText("Exact Zero Line: v = √5 u (unreachable in Z²)", padL + 145, botY + 20);

      ALL880.forEach(function (row) {
        const ux = row[0] + row[2] / 3;
        const uy = row[1] + row[3] / 3;
        const vx = row[0] + row[2];
        const vy = row[1] + row[3];
        const un = Math.hypot(ux, uy);
        const vn = Math.hypot(vx, vy);
        const px = xOfU(un);
        const py = yOfV(vn);
        const isPell = Math.abs(un - 8) < 1e-6 && Math.abs(vn - 18) < 1e-6 && (ux * vx + uy * vy === 144);
        ctxP.fillStyle = isPell ? "#d98200" : "rgba(15, 107, 82, 0.35)";
        ctxP.beginPath();
        ctxP.arc(px, py, isPell ? 4.8 : 2.8, 0, Math.PI * 2);
        ctxP.fill();
      });

      const actX = xOfU(uNorm);
      const actY = yOfV(vNorm);
      ctxP.strokeStyle = "#d91b42";
      ctxP.lineWidth = 2.4;
      ctxP.beginPath();
      ctxP.arc(actX, actY, 7.5, 0, Math.PI * 2);
      ctxP.stroke();

      ctxP.fillStyle = "#3b4845";
      ctxP.font = "11px -apple-system, sans-serif";
      ctxP.fillText("||u|| = ||d_in + d_out/3||₂  (Click any point to inspect)", WP * 0.32, HP - 8);

      // Update readout bar
      const cross = din[0] * dout[1] - din[1] * dout[0];
      const colStr = cross === 0
        ? "Collinear (κ = " + (din[0] !== 0 ? (dout[0] / din[0]).toFixed(2) : (dout[1] / din[1]).toFixed(2)) + ")"
        : "Non-collinear (det = " + cross + ")";
      const ratioStr = uNorm > 1e-6 ? (vNorm / uNorm).toFixed(4) : "∞";
      if (state.viewMode === "3d") {
        readout.innerHTML =
          "<span>Square <strong>" + info.label + "</strong> · 3D Resultant ||V_β||₂ = <span class='" + (res3D.norm < 1e-4 ? "hl" : "warn") + "'>" + res3D.norm.toFixed(6) + "</span></span>" +
          "<span>Sphere Weights w_ij* ∈ <span class='hl'>[" + res3D.wMin.toFixed(3) + ", " + res3D.wMax.toFixed(3) + "]</span> (||w*-1||₂ = " + res3D.wNormDiff.toFixed(3) + ")</span>" +
          "<span>2D Ring Dipoles: " + colStr + " · ||B_{z,ℓ}||₂ = <span class='" + (res.norm < 0.08 ? "hl" : "warn") + "'>" + res.norm.toFixed(5) + "</span></span>";
      } else {
        readout.innerHTML =
          "<span>Square <strong>" + info.label + "</strong>: d_in=(" + din[0] + "," + din[1] + "), d_out=(" + dout[0] + "," + dout[1] + ") · " + colStr + "</span>" +
          "<span>||v||/||u|| = " + vNorm.toFixed(2) + "/" + uNorm.toFixed(2) + " = <span class='hl'>" + ratioStr + "</span> (√5 ≈ 2.2361)</span>" +
          "<span>||B_{z,ℓ}(S)||₂ = <span class='" + (res.norm < 0.08 ? "hl" : "warn") + "'>" + res.norm.toFixed(6) + "</span></span>";
      }
      updateActiveButtons();
    }

    // Click on scatter plot to select any of the 880 squares
    canvasPell.addEventListener("click", function (e) {
      const rect = canvasPell.getBoundingClientRect();
      const mx = (e.clientX - rect.left) * (canvasPell.width / rect.width);
      const my = (e.clientY - rect.top) * (canvasPell.height / rect.height);
      const padL = 48, padR = 20, botY = 212, botH = 195;
      if (my < botY || my > botY + botH) return;
      const maxU = 15.5, maxV = 35.0;
      let bestIdx = -1;
      let bestDist = 999;
      ALL880.forEach(function (row, idx) {
        const un = Math.hypot(row[0] + row[2] / 3, row[1] + row[3] / 3);
        const vn = Math.hypot(row[0] + row[2], row[1] + row[3]);
        const px = padL + (un / maxU) * (canvasPell.width - padL - padR);
        const py = botY + botH - (vn / maxV) * (botH - 10);
        const d = Math.hypot(mx - px, my - py);
        if (d < bestDist) {
          bestDist = d;
          bestIdx = idx;
        }
      });
      if (bestIdx >= 0 && bestDist < 18) {
        state.customIdx0 = bestIdx;
        state.collinearCustomWeights = null;
        renderSim1();
      }
    });

    if (viewModeSelect) {
      viewModeSelect.addEventListener("change", function () {
        state.viewMode = viewModeSelect.value;
        renderSim1();
      });
    }

    sqSelect.addEventListener("change", function () {
      state.sqKey = sqSelect.value;
      state.customIdx0 = null;
      state.collinearCustomWeights = null;
      renderSim1();
    });

    alphaSlider.addEventListener("input", function () {
      state.alpha = parseFloat(alphaSlider.value);
      state.collinearCustomWeights = null;
      state.weightedSphere = false;
      alphaVal.textContent = state.alpha.toFixed(2);
      renderSim1();
    });

    btnAlpha0.addEventListener("click", function () {
      state.alpha = 0.0;
      state.collinearCustomWeights = null;
      state.weightedSphere = false;
      alphaSlider.value = "0.00";
      alphaVal.textContent = "0.00";
      renderSim1();
    });

    btnAlpha1.addEventListener("click", function () {
      state.alpha = 1.0;
      state.collinearCustomWeights = null;
      state.weightedSphere = false;
      alphaSlider.value = "1.00";
      alphaVal.textContent = "1.00";
      renderSim1();
    });

    if (btn3DWeights) {
      btn3DWeights.addEventListener("click", function () {
        state.viewMode = "3d";
        if (viewModeSelect) viewModeSelect.value = "3d";
        state.alpha = 0.0;
        state.weightedSphere = true;
        state.collinearCustomWeights = null;
        alphaSlider.value = "0.00";
        alphaVal.textContent = "0.00 (w*)";
        renderSim1();
      });
    }

    if (btnAlphaM1) {
      btnAlphaM1.addEventListener("click", function () {
        state.sqKey = "45";
        state.customIdx0 = null;
        sqSelect.value = "45";
        if (state.viewMode === "3d") {
          state.viewMode = "polygon";
          if (viewModeSelect) viewModeSelect.value = "polygon";
        }
        state.alpha = -1.0;
        state.weightedSphere = false;
        state.collinearCustomWeights = null;
        alphaSlider.value = "-1.00";
        alphaVal.textContent = "-1.00";
        renderSim1();
      });
    }

    if (btnAlphaP3) {
      btnAlphaP3.addEventListener("click", function () {
        state.sqKey = "286";
        state.customIdx0 = null;
        sqSelect.value = "286";
        if (state.viewMode === "3d") {
          state.viewMode = "polygon";
          if (viewModeSelect) viewModeSelect.value = "polygon";
        }
        state.alpha = 3.0;
        state.weightedSphere = false;
        state.collinearCustomWeights = null;
        alphaSlider.value = "3.00";
        alphaVal.textContent = "3.00";
        renderSim1();
      });
    }

    btnCollinear.addEventListener("click", function () {
      const info = getDipoles();
      const din = info.din;
      const dout = info.dout;
      const cross = din[0] * dout[1] - din[1] * dout[0];
      if (cross !== 0) {
        state.sqKey = "46";
        state.customIdx0 = null;
        sqSelect.value = "46";
      }
      if (state.viewMode === "3d") {
        state.viewMode = "polygon";
        if (viewModeSelect) viewModeSelect.value = "polygon";
      }
      const cur = getDipoles();
      const kappa = cur.din[0] !== 0 ? cur.dout[0] / cur.din[0] : cur.dout[1] / cur.din[1];
      let gamma1, gamma2, gamma3;
      if (kappa < 0) {
        gamma2 = 1.0;
        gamma3 = 1.5;
        gamma1 = 1.0 - 0.5 * kappa;
      } else {
        gamma2 = 1.2;
        gamma3 = 0.7;
        gamma1 = 1.2 + 0.5 * kappa;
      }
      const l1 = RING_RADII[1] * gamma1;
      const l2 = RING_RADII[2] * gamma2;
      const l3 = RING_RADII[3] * gamma3;
      state.collinearCustomWeights = { l1, l2, l3 };
      state.weightedSphere = false;
      alphaVal.textContent = "Tuned";
      renderSim1();
    });

    // ---- Essay additions: view tabs, smooth alpha animation, sweep & external API ----
    const tabBtns = Array.prototype.slice.call(document.querySelectorAll("#ring-tabs .sim-tab"));
    const btnSweep = document.getElementById("btn-ring-sweep");
    let alphaAnim = null;
    let sweep = null;
    watchVisibility("sim-rings");

    function syncTabs() {
      tabBtns.forEach(function (b) { b.classList.toggle("active", b.getAttribute("data-view") === state.viewMode); });
    }
    function setView(v) {
      state.viewMode = v;
      if (viewModeSelect) viewModeSelect.value = v;
      renderSim1();
    }
    tabBtns.forEach(function (b) {
      b.addEventListener("click", function () { setView(b.getAttribute("data-view")); });
    });

    function setAlphaUI(a) {
      state.alpha = a;
      alphaSlider.value = a.toFixed(2);
      alphaVal.textContent = a.toFixed(2);
    }
    function stopSweep() {
      sweep = null;
      if (btnSweep) { btnSweep.classList.remove("active"); btnSweep.textContent = "▶ Sweep α"; }
    }
    function animateAlphaTo(target, dur) {
      stopSweep();
      state.collinearCustomWeights = null;
      state.weightedSphere = false;
      alphaAnim = { from: state.alpha, to: target, t0: performance.now(), dur: dur || 1100 };
    }
    alphaSlider.addEventListener("input", function () { alphaAnim = null; stopSweep(); });

    // Preset buttons glide to their exponent instead of jumping
    [btnAlpha0, btnAlpha1, btnAlphaM1, btnAlphaP3].forEach(function (b) {
      if (!b) return;
      let prev = null;
      b.addEventListener("pointerdown", function () { prev = state.alpha; });
      b.addEventListener("click", function () {
        if (prev === null) return;
        const tgt = state.alpha;
        setAlphaUI(prev);
        prev = null;
        animateAlphaTo(tgt, 900);
      });
    });

    if (btnSweep) {
      btnSweep.addEventListener("click", function () {
        if (sweep) { stopSweep(); return; }
        alphaAnim = null;
        state.collinearCustomWeights = null;
        state.weightedSphere = false;
        const c = Math.max(-1, Math.min(1, (0.95 - state.alpha) / 2.15));
        sweep = { t0: performance.now(), phase0: Math.acos(c) };
        btnSweep.classList.add("active");
        btnSweep.textContent = "⏸ Stop Sweep";
      });
    }

    function ensureOption(v) {
      v = String(v);
      const has = Array.prototype.some.call(sqSelect.options, function (o) { return o.value === v; });
      if (!has) {
        const o = document.createElement("option");
        o.value = v;
        o.textContent = "#" + v;
        sqSelect.appendChild(o);
      }
    }

    window.MG_SIM1 = {
      load: function (o) {
        o = o || {};
        if (o.sq !== undefined) {
          ensureOption(o.sq);
          state.sqKey = String(o.sq);
          state.customIdx0 = null;
          sqSelect.value = state.sqKey;
        }
        state.collinearCustomWeights = null;
        if (o.weights) { stopSweep(); alphaAnim = null; btn3DWeights.click(); return; }
        if (o.view) { state.viewMode = o.view; if (viewModeSelect) viewModeSelect.value = o.view; }
        state.weightedSphere = false;
        if (o.alpha !== undefined && !isNaN(o.alpha)) animateAlphaTo(o.alpha, 1300);
        renderSim1();
      },
      preset: function (name) {
        const P = {
          pell: { sq: 70, view: "polygon", alpha: 0 },
          inv45: { sq: 45, view: "polygon", alpha: -1 },
          cub286: { sq: 286, view: "polygon", alpha: 3 },
          sphereW: { sq: 70, weights: true }
        };
        if (P[name]) this.load(P[name]);
      }
    };

    function sim1Frame(now) {
      if (alphaAnim) {
        const t = Math.min(1, (now - alphaAnim.t0) / alphaAnim.dur);
        setAlphaUI(alphaAnim.from + (alphaAnim.to - alphaAnim.from) * easeInOut(t));
        if (t >= 1) alphaAnim = null;
        renderSim1();
      } else if (sweep && isVisible("sim-rings")) {
        setAlphaUI(0.95 - 2.15 * Math.cos(sweep.phase0 + (2 * Math.PI * (now - sweep.t0)) / 9000));
        renderSim1();
      }
      requestAnimationFrame(sim1Frame);
    }
    requestAnimationFrame(sim1Frame);

    renderSim1();
  }


  // =========================================================================
  // SIMULATOR 2: Zero-Gravity Spin — Magic Gems vs. Cube, Cone, Pyramid & Sphere
  // =========================================================================
  function initSim2() {
    const sqSelect = document.getElementById("rot-sq-select");
    const modelSelect = document.getElementById("rot-model-select");
    const rotTabs = document.getElementById("rot-tabs");
    const lamSlider = document.getElementById("rot-lam-slider");
    const lamVal = document.getElementById("rot-lam-val");
    const btnCube = document.getElementById("btn-lam-cube");
    const btnIso = document.getElementById("btn-lam-iso");
    const btnOne = document.getElementById("btn-lam-one");
    const btnDzh = document.getElementById("btn-dzh-kick");
    const btnCone = document.getElementById("btn-cone-kick");
    const btnEllipsoid = document.getElementById("btn-rot-ellipsoid");
    const btnLens = document.getElementById("btn-rot-lens");
    const btnPause = document.getElementById("btn-rot-pause");
    const canvas3d = document.getElementById("canvas-rot-3d");
    const canvasChart = document.getElementById("canvas-rot-chart");
    const readout = document.getElementById("rot-readout");
    if (!canvas3d || !canvasChart) return;

    const ctx3 = canvas3d.getContext("2d");
    const ctxC = canvasChart.getContext("2d");
    const cam = { yaw: -0.65, pitch: 0.42 };
    attachOrbitControl(canvas3d, cam);
    watchVisibility("sim-precession");

    const HIST = 320;
    const W0 = 2.25; // initial spin rate about the intermediate axis
    const KICKS = {
      dzh: [0.035, W0, 0.035],   // spin about axis 2 with a tiny wobble
      cone: [1.05, 0.0, 1.82],   // classic 30-degree precession cone
      tilt: [0.95, 1.35, 1.15]   // arbitrary off-axis spin
    };
    const PALETTES = {
      point:   { rgb: [15, 118, 110],  ball: "#0f766e", trail: "15,118,110",  text: "#0f766e", name: "Equal Gem",   short: "Equal Gem" },
      entry:   { rgb: [190, 40, 70],   ball: "#e11d48", trail: "225,29,72",   text: "#be123c", name: "Entry Gem",   short: "Entry Gem (m=s)" },
      solid:   { rgb: [29, 78, 216],   ball: "#1d4ed8", trail: "29,78,216",   text: "#1d4ed8", name: "Solid Gem",   short: "Solid Gem" },
      sphere:  { rgb: [2, 132, 199],   ball: "#0284c7", trail: "2,132,199",   text: "#0369a1", name: "Sphere",      short: "Sphere" },
      cube:    { rgb: [124, 58, 237],  ball: "#7c3aed", trail: "124,58,237",  text: "#6d28d9", name: "Perfect Cube",short: "Perfect Cube" },
      cone:    { rgb: [217, 119, 6],   ball: "#d97706", trail: "217,119,6",   text: "#b45309", name: "Cone",        short: "Circular Cone" },
      pyramid: { rgb: [5, 150, 105],   ball: "#059669", trail: "5,150,105",   text: "#047857", name: "Pyramid",     short: "Square Pyramid" }
    };

    // Build canonical 3D meshes for the 4 classical shapes (Sphere, Cube, Cone, Pyramid)
    function buildClassicalMeshes() {
      // 1. Perfect Cube: side 2*a with a = 1.48
      const a = 1.48;
      const cubeVerts = [
        [-a, -a, -a], [ a, -a, -a], [ a,  a, -a], [-a,  a, -a],
        [-a, -a,  a], [ a, -a,  a], [ a,  a,  a], [-a,  a,  a]
      ];
      const cubeFaces = [
        { verts: [0, 3, 2, 1], stripe: 0 },
        { verts: [4, 5, 6, 7], stripe: 1 },
        { verts: [0, 1, 5, 4], stripe: 0 },
        { verts: [2, 3, 7, 6], stripe: 1 },
        { verts: [1, 2, 6, 5], stripe: 0 },
        { verts: [3, 0, 4, 7], stripe: 1 }
      ];

      // 2. Square Pyramid: CM at origin, base at z = -h/4, apex at z = +3h/4
      const pb = 1.72, ph = 2.65;
      const zBase = -0.32 * ph, zApex = 0.68 * ph;
      const pyrVerts = [
        [-pb, -pb, zBase], [ pb, -pb, zBase], [ pb,  pb, zBase], [-pb,  pb, zBase],
        [0, 0, zApex]
      ];
      const pyrFaces = [
        { verts: [0, 3, 2, 1], stripe: 0 },
        { verts: [0, 1, 4], stripe: 1 },
        { verts: [1, 2, 4], stripe: 0 },
        { verts: [2, 3, 4], stripe: 1 },
        { verts: [3, 0, 4], stripe: 0 }
      ];

      // 3. Right Circular Cone: 12-gon base at z = zBase, apex at z = zApex
      const N = 12, cr = 1.72, ch = 2.70;
      const czB = -0.32 * ch, czA = 0.68 * ch;
      const coneVerts = [];
      for (let k = 0; k < N; k++) {
        const th = (2 * Math.PI * k) / N;
        coneVerts.push([cr * Math.cos(th), cr * Math.sin(th), czB]);
      }
      coneVerts.push([0, 0, czA]); // index N = apex
      const coneFaces = [];
      const baseRing = [];
      for (let k = N - 1; k >= 0; k--) baseRing.push(k);
      coneFaces.push({ verts: baseRing, stripe: 0 });
      for (let k = 0; k < N; k++) {
        coneFaces.push({ verts: [k, (k + 1) % N, N], stripe: k % 2 });
      }

      // 4. Faceted UV Sphere with alternating longitude beach-ball bands so spin is unmistakable
      const nLat = 6, nLon = 12, sr = 1.82;
      const sphVerts = [[0, 0, -sr], [0, 0, sr]]; // 0 = south pole, 1 = north pole
      for (let i = 1; i < nLat; i++) {
        const phi = -0.5 * Math.PI + (Math.PI * i) / nLat;
        const cosp = Math.cos(phi), sinp = Math.sin(phi);
        for (let j = 0; j < nLon; j++) {
          const th = (2 * Math.PI * j) / nLon;
          sphVerts.push([sr * cosp * Math.cos(th), sr * cosp * Math.sin(th), sr * sinp]);
        }
      }
      const ringIdx = function (i, j) { return 2 + (i - 1) * nLon + (j % nLon); };
      const sphFaces = [];
      for (let j = 0; j < nLon; j++) {
        sphFaces.push({ verts: [0, ringIdx(1, j + 1), ringIdx(1, j)], stripe: j % 2 });
        sphFaces.push({ verts: [1, ringIdx(nLat - 1, j), ringIdx(nLat - 1, j + 1)], stripe: j % 2 });
      }
      for (let i = 1; i < nLat - 1; i++) {
        for (let j = 0; j < nLon; j++) {
          sphFaces.push({
            verts: [ringIdx(i, j), ringIdx(i, j + 1), ringIdx(i + 1, j + 1), ringIdx(i + 1, j)],
            stripe: (j + i) % 2
          });
        }
      }

      return {
        cube:    { verts: cubeVerts, faces: cubeFaces },
        pyramid: { verts: pyrVerts,  faces: pyrFaces },
        cone:    { verts: coneVerts, faces: coneFaces },
        sphere:  { verts: sphVerts,  faces: sphFaces }
      };
    }
    const CLASSICAL_MESHES = buildClassicalMeshes();
    const ALL_MODELS = ["point", "entry", "solid", "sphere", "cube", "cone", "pyramid"];

    function newBody(kick) {
      return {
        R: [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        omega: (KICKS[kick] || KICKS.dzh).slice(),
        trail: [],
        history: [],
        flips: 0,
        lastSign: 0
      };
    }

    function newBodyMap(kick) {
      const m = {};
      ALL_MODELS.forEach(function (k) { m[k] = newBody(kick); });
      return m;
    }

    const state = {
      sqKey: sqSelect.value || "46",
      model: modelSelect.value || "compare",
      lambda: 1 / Math.sqrt(17),
      kick: "dzh",
      paused: false,
      showEllipsoid: true,
      showLens: true,
      bodies: newBodyMap("dzh")
    };

    function getGem() { return GEMS[state.sqKey] || GEMS["46"]; }

    // Diagonal quadrupole Q_xy = sum z_ij x_j y_i (always an integer for magic squares)
    function qxyOf(S) {
      let q = 0;
      for (let i = 0; i < 4; i++) {
        for (let j = 0; j < 4; j++) q += (S[i][j] - 8.5) * (-1.5 + j) * (1.5 - i);
      }
      return Math.round(q);
    }

    function momentsFor(model) {
      const gem = getGem();
      const lam = state.lambda;
      if (model === "point") {
        // Theorem 3.1 (scaled by 1/16): I_perp = a_n + lam^2 b_n, I_zz = 2 a_n
        const Iperp = 1.25 * (1 + 17 * lam * lam);
        return { I1: Iperp, I2: Iperp, I3: 2.5, q: 0 };
      }
      if (model === "entry") {
        // Theorem 3.2 (scaled by 1/136): I_1 = 170 - |Q|, I_2 = 170 + |Q|, I_3 = 340
        const q = Math.abs(qxyOf(gem.S));
        return { I1: (170 - q) / 136, I2: (170 + q) / 136, I3: 340 / 136, q: q };
      }
      if (model === "sphere") {
        // Uniform sphere: I_1 = I_2 = I_3 = 2/5 M R^2 (normalized to 2.50)
        return { I1: 2.5, I2: 2.5, I3: 2.5, q: 0 };
      }
      if (model === "cube") {
        // Uniform perfect cube: I_1 = I_2 = I_3 = 1/6 M a^2 — exact spherical top.
        return { I1: 2.5, I2: 2.5, I3: 2.5, q: 0 };
      }
      if (model === "cone") {
        // Right circular cone of height/radius ratio h/R = 2.6 -> symmetric top (I_1 = I_2 > I_3)
        // I_perp / I_zz = 1/2 + (1/8)(h/R)^2 = 1.345
        return { I1: 2.69, I2: 2.69, I3: 2.00, q: 0 };
      }
      if (model === "pyramid") {
        // Regular square pyramid (C_4 symmetry) -> symmetric top (I_1 = I_2 != I_3)
        return { I1: 2.15, I2: 2.15, I3: 2.50, q: 0 };
      }
      const cov = gem.cov0;
      const sc = [1, 1, lam];
      const S = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
      ];
      for (let r = 0; r < 3; r++) {
        for (let c = 0; c < 3; c++) {
          S[r][c] = cov[r][c] * sc[r] * sc[c];
        }
      }
      const trS = S[0][0] + S[1][1] + S[2][2];
      const Imat = [
        [trS - S[0][0], -S[0][1], -S[0][2]],
        [-S[1][0], trS - S[1][1], -S[1][2]],
        [-S[2][0], -S[2][1], trS - S[2][2]]
      ];
      const eig = jacobiEigen3x3(Imat);
      return { I1: eig.vals[0], I2: eig.vals[1], I3: eig.vals[2], q: 0, axes: eig.vecs };
    }

    function modelsActive() {
      const m = state.model;
      if (m === "compare") return ["point", "entry"];
      if (m === "vs-sphere") return ["point", "sphere"];
      if (m === "vs-cube") return ["point", "cube"];
      if (m === "vs-cone") return ["point", "cone"];
      if (m === "vs-pyramid") return ["point", "pyramid"];
      if (m === "gallery") return ["point", "entry", "sphere", "cube", "cone", "pyramid"];
      return [m];
    }

    function syncTabs() {
      if (!rotTabs) return;
      rotTabs.querySelectorAll(".sim-tab").forEach(function (btn) {
        btn.classList.toggle("active", btn.getAttribute("data-rot-mode") === state.model);
      });
    }

    function resetKick(kick) {
      if (kick) state.kick = kick;
      state.bodies = newBodyMap(state.kick);
    }

    function stepBody(body, mom, dt) {
      const I1 = mom.I1, I2 = mom.I2, I3 = mom.I3;
      function dW(w) {
        return [
          ((I2 - I3) / I1) * w[1] * w[2],
          ((I3 - I1) / I2) * w[2] * w[0],
          ((I1 - I2) / I3) * w[0] * w[1]
        ];
      }
      const w0 = body.omega;
      const k1 = dW(w0);
      const k2 = dW(vecAdd(w0, vecScale(k1, 0.5 * dt)));
      const k3 = dW(vecAdd(w0, vecScale(k2, 0.5 * dt)));
      const k4 = dW(vecAdd(w0, vecScale(k3, dt)));
      body.omega = [0, 1, 2].map(function (c) {
        return w0[c] + (dt / 6) * (k1[c] + 2 * k2[c] + 2 * k3[c] + k4[c]);
      });
      const wMid = [
        0.5 * (w0[0] + body.omega[0]),
        0.5 * (w0[1] + body.omega[1]),
        0.5 * (w0[2] + body.omega[2])
      ];
      body.R = matMul(body.R, rodriguesExp(wMid, dt));
      body.trail.push(matVec(body.R, [0, 2.3, 0]));
      if (body.trail.length > 260) body.trail.shift();
      body.history.push({ w1: body.omega[0], w2: body.omega[1], w3: body.omega[2] });
      if (body.history.length > HIST) body.history.shift();
      // Count 180-degree flips of the intermediate-axis spin (with hysteresis)
      if (state.kick === "dzh") {
        const w2 = body.omega[1];
        if (Math.abs(w2) > 0.6 * W0) {
          const s = w2 > 0 ? 1 : -1;
          if (body.lastSign !== 0 && s !== body.lastSign) body.flips++;
          body.lastSign = s;
        }
      }
    }

    // Body frame: align body axes with the principal inertia axes (exact diagonal for point/entry, Jacobi eigenvectors for solid)
    function bodyFrame(gem, model) {
      if (model === "solid") {
        const mom = momentsFor("solid");
        return { e1: mom.axes[0], e2: mom.axes[1], e3: mom.axes[2] };
      }
      if (model !== "point" && model !== "entry") return { e1: [1, 0, 0], e2: [0, 1, 0], e3: [0, 0, 1] };
      const s = qxyOf(gem.S) >= 0 ? 1 : -1;
      return {
        e1: [Math.SQRT1_2, s * Math.SQRT1_2, 0],
        e2: [-s * Math.SQRT1_2, Math.SQRT1_2, 0],
        e3: [0, 0, 1]
      };
    }

    function drawRotor(body, model, cx, cy, scale, title, compact) {
      const gem = getGem();
      const pal = PALETTES[model] || PALETTES.point;
      const classical = CLASSICAL_MESHES[model];
      const effScale = (!classical && state.lambda > 0.55)
        ? scale * (0.55 / (0.55 + 0.45 * (state.lambda - 0.55)))
        : scale;
      const P = function (pt) {
        const q = project3D(pt, cam, 0, 0, effScale);
        return { x: cx + q.x, y: cy + q.y, depth: q.depth };
      };

      // Spin axis (body axis 2) as a dashed stick
      const axLen = compact ? 2.45 : 2.7;
      const axTip = matVec(body.R, [0, axLen, 0]);
      const pA = P(axTip), pB = P(vecScale(axTip, -1));
      ctx3.save();
      ctx3.strokeStyle = "rgba(225, 29, 72, 0.5)";
      ctx3.lineWidth = compact ? 1.5 : 2;
      ctx3.setLineDash([4, 3]);
      ctx3.beginPath(); ctx3.moveTo(pB.x, pB.y); ctx3.lineTo(pA.x, pA.y); ctx3.stroke();
      ctx3.restore();

      // Fading trail of the axis tip
      const tr = body.trail;
      const stepK = compact ? 2 : 1;
      for (let k = stepK; k < tr.length; k += stepK) {
        const a = P(tr[k - stepK]), b = P(tr[k]);
        ctx3.strokeStyle = "rgba(" + pal.trail + "," + (0.08 + 0.8 * k / tr.length).toFixed(3) + ")";
        ctx3.lineWidth = compact ? 1.5 : 2;
        ctx3.beginPath(); ctx3.moveTo(a.x, a.y); ctx3.lineTo(b.x, b.y); ctx3.stroke();
      }

      const items = [];
      if (classical) {
        const world = classical.verts.map(function (v) { return matVec(body.R, v); });
        classical.faces.forEach(function (f) {
          const pts = f.verts.map(function (vi) { return world[vi]; });
          let c = [0, 0, 0];
          pts.forEach(function (p) { c = vecAdd(c, p); });
          c = vecScale(c, 1 / pts.length);
          const n = vecNormalize(vecCross(vecSub(pts[1], pts[0]), vecSub(pts[2], pts[0])));
          items.push({
            kind: "face",
            pts: pts,
            depth: P(c).depth,
            light: Math.abs(n[0] * 0.4 - n[1] * 0.5 + n[2] * 0.75),
            stripe: f.stripe || 0
          });
        });
        if (model === "cube" || model === "pyramid") {
          world.forEach(function (w) {
            items.push({ kind: "ball", p: w, s: 6, depth: P(w).depth + 0.05 });
          });
        }
      } else {
        const fr = bodyFrame(gem, model);
        const visLam = Math.max(0.16, state.lambda);
        const e3 = fr.e3 || [0, 0, 1];
        const cOff = (model === "solid" && gem.c0) ? [gem.c0[0], gem.c0[1], gem.c0[2] * visLam] : [0, 0, 0];
        const world = gem.P_real.map(function (p) {
          const ps = [p[0] - cOff[0], p[1] - cOff[1], p[2] * visLam - cOff[2]];
          const b = [
            vecDot(ps, fr.e1),
            vecDot(ps, fr.e2),
            vecDot(ps, e3)
          ];
          return matVec(body.R, b);
        });
        gem.faces0.forEach(function (f) {
          const pts = f.verts.map(function (vi) { return world[vi]; });
          let c = [0, 0, 0];
          pts.forEach(function (p) { c = vecAdd(c, p); });
          c = vecScale(c, 1 / pts.length);
          const n = vecNormalize(vecCross(vecSub(pts[1], pts[0]), vecSub(pts[2], pts[0])));
          items.push({
            kind: "face",
            pts: pts,
            depth: P(c).depth,
            light: Math.abs(n[0] * 0.4 - n[1] * 0.5 + n[2] * 0.75),
            stripe: 0
          });
        });
        if (model !== "solid") {
          world.forEach(function (w, k) {
            const s = gem.S[Math.floor(k / 4)][k % 4];
            items.push({ kind: "ball", p: w, s: s, depth: P(w).depth + 0.05 });
          });
        }
      }

      items.sort(function (a, b) { return a.depth - b.depth; });
      items.forEach(function (it) {
        if (it.kind === "face") {
          const stripeBoost = it.stripe ? 28 : 0;
          const f = 0.52 + 0.46 * it.light;
          const rC = Math.min(255, Math.round(pal.rgb[0] * f + 38 + stripeBoost));
          const gC = Math.min(255, Math.round(pal.rgb[1] * f + 38 + stripeBoost));
          const bC = Math.min(255, Math.round(pal.rgb[2] * f + 38 + stripeBoost));
          ctx3.fillStyle = "rgba(" + rC + "," + gC + "," + bC + "," + (classical ? "0.72" : "0.62") + ")";
          ctx3.strokeStyle = "rgba(16, 37, 38, 0.48)";
          ctx3.lineWidth = compact ? 0.75 : 1;
          ctx3.beginPath();
          it.pts.forEach(function (p, i) {
            const q = P(p);
            if (i === 0) ctx3.moveTo(q.x, q.y); else ctx3.lineTo(q.x, q.y);
          });
          ctx3.closePath();
          ctx3.fill();
          ctx3.stroke();
        } else {
          const q = P(it.p);
          const rBase = model === "entry" ? 1.6 + it.s * 0.32 : 3.2;
          const r = compact ? rBase * 0.72 : rBase;
          ctx3.fillStyle = pal.ball;
          ctx3.strokeStyle = "#ffffff";
          ctx3.lineWidth = 0.9;
          ctx3.beginPath(); ctx3.arc(q.x, q.y, r, 0, Math.PI * 2); ctx3.fill(); ctx3.stroke();
        }
      });

      // Conserved angular momentum L
      const mom = momentsFor(model);
      const Lw = vecNormalize(matVec(body.R, [mom.I1 * body.omega[0], mom.I2 * body.omega[1], mom.I3 * body.omega[2]]));
      const pL = P(vecScale(Lw, compact ? 2.55 : 3.0));
      drawArrow2D(ctx3, cx, cy, pL.x, pL.y, "#0f2528", compact ? 1.8 : 2.4, compact ? 6 : 8);

      // Co-rotating 3D Principal-Plane Inertia Ellipsoid (semi-axes ~ 1/sqrt(I_k))
      if (state.showEllipsoid) {
        const rBase = compact ? 1.72 : 1.92;
        const a1 = rBase * Math.max(0.42, Math.min(1.42, Math.sqrt(2.5 / Math.max(0.2, mom.I1))));
        const a2 = rBase * Math.max(0.42, Math.min(1.42, Math.sqrt(2.5 / Math.max(0.2, mom.I2))));
        const a3 = rBase * Math.max(0.42, Math.min(1.42, Math.sqrt(2.5 / Math.max(0.2, mom.I3))));
        const planes = [
          { col: "rgba(" + pal.trail + ",0.58)", dash: [4, 3], pt: function (th) { return [a1 * Math.cos(th), a2 * Math.sin(th), 0]; } },
          { col: "rgba(" + pal.trail + ",0.40)", dash: [2, 3], pt: function (th) { return [a1 * Math.cos(th), 0, a3 * Math.sin(th)]; } },
          { col: "rgba(" + pal.trail + ",0.40)", dash: [2, 3], pt: function (th) { return [0, a2 * Math.cos(th), a3 * Math.sin(th)]; } }
        ];
        ctx3.save();
        ctx3.lineWidth = compact ? 1.05 : 1.35;
        planes.forEach(function (pl) {
          ctx3.strokeStyle = pl.col;
          ctx3.setLineDash(pl.dash);
          ctx3.beginPath();
          for (let s = 0; s <= 40; s++) {
            const th = (2 * Math.PI * s) / 40;
            const wPt = matVec(body.R, pl.pt(th));
            const q = P(wPt);
            if (s === 0) ctx3.moveTo(q.x, q.y);
            else ctx3.lineTo(q.x, q.y);
          }
          ctx3.stroke();
        });
        ctx3.restore();
      }

      // Title + live moments
      ctx3.save();
      ctx3.textAlign = "center";
      ctx3.fillStyle = pal.text;
      const topTitleY = compact ? cy - 78 : 22;
      const subTitleY = compact ? cy - 64 : 38;
      const footY = compact ? cy + 80 : canvas3d.height - 14;
      ctx3.font = (compact ? "bold 11.5px " : "bold 12.5px ") + "-apple-system, sans-serif";
      ctx3.fillText(title, cx, topTitleY);
      ctx3.font = (compact ? "9.8px " : "11px ") + "-apple-system, sans-serif";
      ctx3.fillStyle = "#3b4b48";
      const iso = Math.abs(mom.I1 - mom.I2) < 1e-6 && Math.abs(mom.I1 - mom.I3) < 0.02;
      const sym = Math.abs(mom.I1 - mom.I2) < 1e-6 && !iso;
      if (compact) {
        const tag = iso ? "I₁=I₂=I₃ (spherical top)" : (sym ? "I₁=I₂≠I₃ (symmetric cone)" : "I₁<I₂<I₃ (triaxial flips)");
        ctx3.fillText(tag, cx, subTitleY);
      } else {
        ctx3.fillText(
          "I₁=" + mom.I1.toFixed(2) + "  I₂=" + mom.I2.toFixed(2) + "  I₃=" + mom.I3.toFixed(2) + (iso ? "  (spherical top)" : (sym ? "  (symmetric top)" : "")),
          cx, subTitleY
        );
      }
      if (state.kick === "dzh") {
        const flipped = body.flips > 0;
        ctx3.fillStyle = flipped ? "#e11d48" : (sym ? "#b45309" : "#0f766e");
        ctx3.font = (compact ? "bold 10.5px " : "bold 12px ") + "-apple-system, sans-serif";
        const statusTxt = flipped
          ? "⟲ " + body.flips + " flip" + (body.flips === 1 ? "" : "s")
          : (iso ? "✓ zero wobble" : "✓ steady spin (0 flips)");
        ctx3.fillText(statusTxt, cx, footY);
      } else {
        ctx3.fillStyle = iso ? "#0f766e" : (sym ? "#b45309" : "#be123c");
        ctx3.font = (compact ? "bold 10.5px " : "bold 11.5px ") + "-apple-system, sans-serif";
        ctx3.fillText(iso ? "✓ fixed axis (no cone)" : (sym ? "↻ smooth circular cone" : "↯ triaxial wobble"), cx, footY);
      }
      ctx3.restore();
    }

    function renderChart() {
      const WC = canvasChart.width, HC = canvasChart.height;
      ctxC.clearRect(0, 0, WC, HC);
      const padL = 46, padR = 18, topY = 30, topH = 140;
      ctxC.fillStyle = "#132a2c";
      ctxC.font = "bold 12px -apple-system, sans-serif";
      ctxC.fillText("Inertia ratio I⊥ / I_zz: Magic Gem curve vs. Cube, Sphere, Cone & Pyramid", 14, 18);
      ctxC.strokeStyle = "#cbd5d0";
      ctxC.strokeRect(padL, topY, WC - padL - padR, topH);
      const xOfLam = function (l) { return padL + (l / 1.02) * (WC - padL - padR); };
      const yOfR = function (r) { return topY + topH - (r / 9.6) * (topH - 10); };

      // Reference horizontal lines for Sphere/Cube (ratio = 1.0) and Cone (1.35) / Pyramid (0.86)
      ctxC.save();
      ctxC.strokeStyle = "#7c3aed";
      ctxC.setLineDash([4, 4]);
      ctxC.beginPath(); ctxC.moveTo(padL, yOfR(1)); ctxC.lineTo(WC - padR, yOfR(1)); ctxC.stroke();
      ctxC.fillStyle = "#6d28d9";
      ctxC.font = "10px -apple-system, sans-serif";
      ctxC.fillText("Sphere & Perfect Cube (I⊥/I_zz = 1)", padL + 225, yOfR(1) - 5);
      ctxC.restore();

      ctxC.strokeStyle = "#0f766e";
      ctxC.lineWidth = 2.3;
      ctxC.beginPath();
      for (let k = 0; k <= 100; k++) {
        const l = k / 100;
        const xx = xOfLam(l), yy = yOfR(0.5 * (1 + 17 * l * l));
        if (k === 0) ctxC.moveTo(xx, yy); else ctxC.lineTo(xx, yy);
      }
      ctxC.stroke();
      ctxC.lineWidth = 1;
      [[0.2, "λ=0.20 (0.84)"], [1 / Math.sqrt(17), "λ_iso=1/√17"], [1.0, "λ=1: 9"]].forEach(function (m, idx) {
        const xx = xOfLam(m[0]), yy = yOfR(0.5 * (1 + 17 * m[0] * m[0]));
        ctxC.fillStyle = "#5c696d";
        ctxC.beginPath(); ctxC.arc(xx, yy, 3, 0, Math.PI * 2); ctxC.fill();
        ctxC.font = "10px -apple-system, sans-serif";
        ctxC.fillText(m[1], xx + (idx === 2 ? -40 : (idx === 0 ? -62 : -26)), yy + (idx === 0 ? 12 : (idx === 1 ? -15 : -7)));
      });
      // Classical Cone & Pyramid markers on the curve
      [
        { lam: Math.sqrt((2 * 0.86 - 1) / 17), r: 0.86, col: "#059669", lbl: "Pyramid (0.86)", dx: 8, dy: 11 },
        { lam: Math.sqrt((2 * 1.345 - 1) / 17), r: 1.345, col: "#d97706", lbl: "Cone (1.35)", dx: 9, dy: -4 }
      ].forEach(function (mk) {
        const xx = xOfLam(mk.lam), yy = yOfR(mk.r);
        ctxC.fillStyle = mk.col;
        ctxC.beginPath(); ctxC.arc(xx, yy, 4, 0, Math.PI * 2); ctxC.fill();
        ctxC.font = "bold 9.5px -apple-system, sans-serif";
        ctxC.fillText(mk.lbl, xx + mk.dx, yy + mk.dy);
      });

      const lam = state.lambda;
      ctxC.fillStyle = "#e11d48";
      ctxC.beginPath(); ctxC.arc(xOfLam(lam), yOfR(Math.min(9.4, 0.5 * (1 + 17 * lam * lam))), 6, 0, Math.PI * 2); ctxC.fill();
      ctxC.fillStyle = "#3b4b48";
      ctxC.font = "10.5px -apple-system, sans-serif";
      ctxC.fillText("lift scale λ →", WC - padR - 72, topY + topH - 6);

      // Live waveforms
      const botY = 212, botH = 180;
      const active = modelsActive();
      const wKey = state.kick === "cone" ? "w1" : "w2";
      ctxC.fillStyle = "#132a2c";
      ctxC.font = "bold 12px -apple-system, sans-serif";
      ctxC.fillText(
        active.length > 1
          ? (state.kick === "cone"
              ? "Transverse spin ω₁(t) during 30° cone: Sphere & Cube stay flat, Cone/Pyramid oscillate"
              : "Intermediate-axis spin ω₂(t): Sphere, Cube, Cone & Pyramid stay steady; Entry Gem flips")
          : "Body-frame spin components ω₁(t), ω₂(t), ω₃(t) for " + PALETTES[active[0]].short,
        14, botY - 10
      );
      ctxC.strokeStyle = "#cbd5d0";
      ctxC.strokeRect(padL, botY, WC - padL - padR, botH);
      const midY = botY + botH / 2;
      ctxC.strokeStyle = "#e2e8e5";
      ctxC.beginPath(); ctxC.moveTo(padL, midY); ctxC.lineTo(WC - padR, midY); ctxC.stroke();
      ctxC.fillStyle = "#5c696d";
      ctxC.font = "10px -apple-system, sans-serif";
      ctxC.fillText("+", padL - 12, botY + 12);
      ctxC.fillText("−", padL - 12, botY + botH - 4);

      function plot(hist, key, color, norm, dashed) {
        ctxC.save();
        ctxC.strokeStyle = color;
        ctxC.lineWidth = 2;
        if (dashed) ctxC.setLineDash(dashed);
        ctxC.beginPath();
        hist.forEach(function (h, i) {
          const xx = padL + (i / HIST) * (WC - padL - padR);
          const yy = midY - (h[key] / norm) * (botH * 0.44);
          if (i === 0) ctxC.moveTo(xx, yy); else ctxC.lineTo(xx, yy);
        });
        ctxC.stroke();
        ctxC.restore();
      }
      ctxC.font = "bold 10.5px -apple-system, sans-serif";
      if (active.length === 2) {
        const m0 = active[0], m1 = active[1];
        plot(state.bodies[m0].history, wKey, PALETTES[m0].ball, W0 * 1.05);
        plot(state.bodies[m1].history, wKey, PALETTES[m1].ball, W0 * 1.05, m0 === "point" && (m1 === "sphere" || m1 === "cube") ? [5, 4] : null);
        ctxC.fillStyle = PALETTES[m0].text;
        ctxC.fillText("― " + PALETTES[m0].short + " (" + state.bodies[m0].flips + " flips)", padL + 6, botY + botH + 16);
        ctxC.fillStyle = PALETTES[m1].text;
        ctxC.fillText("― " + PALETTES[m1].short + " (" + state.bodies[m1].flips + " flips)", padL + 235, botY + botH + 16);
      } else if (active.length > 2) {
        // 6-shape gallery traces
        plot(state.bodies.point.history, wKey, PALETTES.point.ball, W0 * 1.05);
        plot(state.bodies.cube.history, wKey, PALETTES.cube.ball, W0 * 1.05, [4, 4]);
        plot(state.bodies.cone.history, wKey, PALETTES.cone.ball, W0 * 1.05);
        plot(state.bodies.pyramid.history, wKey, PALETTES.pyramid.ball, W0 * 1.05, [2, 3]);
        plot(state.bodies.entry.history, wKey, PALETTES.entry.ball, W0 * 1.05);
        const leg = [
          { col: PALETTES.point.text, txt: "― Equal Gem / Sphere / Cube" },
          { col: PALETTES.cone.text, txt: "― Cone / Pyramid" },
          { col: PALETTES.entry.text, txt: "― Entry Gem (" + state.bodies.entry.flips + " flips)" }
        ];
        leg.forEach(function (it, idx) {
          ctxC.fillStyle = it.col;
          ctxC.fillText(it.txt, padL + idx * 165, botY + botH + 16);
        });
      } else {
        const b = state.bodies[active[0]];
        plot(b.history, "w1", "#0f766e", 2.6);
        plot(b.history, "w2", "#e11d48", 2.6);
        plot(b.history, "w3", "#1d4ed8", 2.6);
        ctxC.fillStyle = "#0f766e"; ctxC.fillText("― ω₁", padL + 6, botY + botH + 16);
        ctxC.fillStyle = "#e11d48"; ctxC.fillText("― ω₂ (spin axis)", padL + 60, botY + botH + 16);
        ctxC.fillStyle = "#1d4ed8"; ctxC.fillText("― ω₃", padL + 210, botY + botH + 16);
      }
    }

    function render() {
      const W = canvas3d.width, H = canvas3d.height;
      ctx3.clearRect(0, 0, W, H);
      const gem = getGem();
      const active = modelsActive();

      if (active.length === 2) {
        ctx3.strokeStyle = "#e2e8e5";
        ctx3.beginPath(); ctx3.moveTo(W / 2, 46); ctx3.lineTo(W / 2, H - 28); ctx3.stroke();
        const m0 = active[0], m1 = active[1];
        const t0 = (m0 === "point" || m0 === "entry" || m0 === "solid") ? PALETTES[m0].short + " · #" + gem.idx1 : PALETTES[m0].short;
        const t1 = (m1 === "point" || m1 === "entry" || m1 === "solid") ? PALETTES[m1].short + " · #" + gem.idx1 : PALETTES[m1].short;
        drawRotor(state.bodies[m0], m0, W * 0.25, H * 0.52, 44, t0, false);
        drawRotor(state.bodies[m1], m1, W * 0.75, H * 0.52, 44, t1, false);
      } else if (active.length === 6) {
        // 3x2 Arena Grid comparing Magic Gems with Sphere, Cube, Cone & Pyramid
        ctx3.strokeStyle = "#e2e8e5";
        ctx3.beginPath();
        ctx3.moveTo(W / 3, 12); ctx3.lineTo(W / 3, H - 12);
        ctx3.moveTo((2 * W) / 3, 12); ctx3.lineTo((2 * W) / 3, H - 12);
        ctx3.moveTo(14, H / 2); ctx3.lineTo(W - 14, H / 2);
        ctx3.stroke();
        const cells = [
          { m: "point",   cx: W * (1 / 6), cy: H * 0.25, title: "Equal Gem #" + gem.idx1 },
          { m: "sphere",  cx: W * (3 / 6), cy: H * 0.25, title: "Classical Sphere" },
          { m: "cube",    cx: W * (5 / 6), cy: H * 0.25, title: "Perfect Cube" },
          { m: "cone",    cx: W * (1 / 6), cy: H * 0.75, title: "Right Circular Cone" },
          { m: "pyramid", cx: W * (3 / 6), cy: H * 0.75, title: "Square Pyramid" },
          { m: "entry",   cx: W * (5 / 6), cy: H * 0.75, title: "Entry Gem #" + gem.idx1 }
        ];
        cells.forEach(function (c) {
          drawRotor(state.bodies[c.m], c.m, c.cx, c.cy + 4, 24.5, c.title, true);
        });
      } else {
        const m0 = active[0];
        const t0 = (m0 === "point" || m0 === "entry" || m0 === "solid") ? PALETTES[m0].short + " · #" + gem.idx1 : PALETTES[m0].short;
        drawRotor(state.bodies[m0], m0, W * 0.5, H * 0.52, 64, t0, false);
      }
      if (state.showLens && active.length !== 6) {
        drawSquareLensHUD(ctx3, gem.S, {
          show: true,
          mode: "quadrupole",
          title: "#" + gem.idx1 + " (Q_xy=" + qxyOf(gem.S) + ")",
          x: 10,
          y: 44,
          cellSz: 19
        });
      }
      renderChart();

      // Update bottom readout bar
      const mP = momentsFor("point");
      const mE = momentsFor("entry");
      const gamma = Math.sqrt(mE.q / 170);
      if (state.model === "compare") {
        readout.innerHTML =
          "<span>Equal Gem: <span class='hl'>I₁ = I₂ = " + mP.I1.toFixed(2) + "</span> → symmetric/spherical top, never flips</span>" +
          "<span>Entry Gem: <span class='" + (mE.q > 0 ? "warn" : "hl") + "'>I₁=" + mE.I1.toFixed(2) + " &lt; I₂=" + mE.I2.toFixed(2) + " &lt; I₃=" + mE.I3.toFixed(2) + "</span> (|Q_xy| = " + mE.q + ", Γ = " + gamma.toFixed(3) + ")</span>" +
          "<span>Flips: <span class='gold'>Equal " + state.bodies.point.flips + " · Entry " + state.bodies.entry.flips + "</span></span>";
      } else if (state.model === "gallery") {
        readout.innerHTML =
          "<span>Spherical Tops (<span class='hl'>I₁=I₂=I₃</span>): Sphere, Perfect Cube &amp; Equal Gem at λ=1/√17 (0 wobble, 0 flips)</span>" +
          "<span>Symmetric Tops (<span class='gold'>I₁=I₂≠I₃</span>): Cone &amp; Pyramid (smooth precession cone, 0 flips)</span>" +
          "<span>Triaxial (<span class='warn'>I₁&lt;I₂&lt;I₃</span>): Entry Gem #" + gem.idx1 + " (<span class='warn'>" + state.bodies.entry.flips + " flips</span>)</span>";
      } else if (active.length === 2) {
        const m1 = active[1];
        const mom1 = momentsFor(m1);
        const desc1 = (m1 === "sphere" || m1 === "cube")
          ? "exact spherical top (I₁=I₂=I₃=2.50, zero wobble)"
          : "axisymmetric top (I₁=I₂=" + mom1.I1.toFixed(2) + ", I₃=" + mom1.I3.toFixed(2) + ", smooth cone)";
        readout.innerHTML =
          "<span>Equal Gem #" + gem.idx1 + ": <span class='hl'>I₁=I₂=" + mP.I1.toFixed(2) + ", I₃=2.50</span> (" + (Math.abs(mP.I1 - 2.5) < 0.02 ? "spherical top" : "symmetric top") + ")</span>" +
          "<span>" + PALETTES[m1].short + ": <span class='hl'>" + desc1 + "</span></span>" +
          "<span>Flips: <span class='gold'>Gem " + state.bodies.point.flips + " · " + PALETTES[m1].name + " " + state.bodies[m1].flips + "</span></span>";
      } else {
        const m0 = active[0];
        const mA = momentsFor(m0);
        const isIso = Math.abs(mA.I1 - mA.I2) < 1e-4 && Math.abs(mA.I1 - mA.I3) < 0.02;
        const tri = Math.abs(mA.I1 - mA.I2) > 1e-3;
        readout.innerHTML =
          "<span>" + PALETTES[m0].short + " Moments: <span class='hl'>I₁=" + mA.I1.toFixed(3) + ", I₂=" + mA.I2.toFixed(3) + ", I₃=" + mA.I3.toFixed(3) + "</span></span>" +
          "<span>Regime: <span class='" + (tri ? "warn" : "hl") + "'>" +
          (isIso ? "Spherical top (zero wobble around any axis)" : (tri ? "Three distinct moments: Dzhanibekov flips" : "Symmetric top: smooth circular precession")) + "</span></span>" +
          "<span>Flips: <span class='gold'>" + state.bodies[m0].flips + "</span></span>";
      }
    }

    function setLam(v, btn) {
      state.lambda = v;
      lamSlider.value = v.toFixed(4);
      lamVal.textContent = v.toFixed(4);
      [btnCube, btnIso, btnOne].forEach(function (b) { b.classList.toggle("active", b === btn); });
    }

    function setMode(m) {
      state.model = m;
      modelSelect.value = m;
      syncTabs();
      resetKick();
    }

    if (rotTabs) {
      rotTabs.querySelectorAll(".sim-tab").forEach(function (btn) {
        btn.addEventListener("click", function () {
          setMode(btn.getAttribute("data-rot-mode"));
        });
      });
    }
    sqSelect.addEventListener("change", function () { state.sqKey = sqSelect.value; resetKick(); });
    modelSelect.addEventListener("change", function () { state.model = modelSelect.value; syncTabs(); resetKick(); });
    lamSlider.addEventListener("input", function () { setLam(parseFloat(lamSlider.value), null); });
    btnCube.addEventListener("click", function () { setLam(0.2, btnCube); });
    btnIso.addEventListener("click", function () { setLam(1 / Math.sqrt(17), btnIso); });
    btnOne.addEventListener("click", function () { setLam(1.0, btnOne); });
    btnDzh.addEventListener("click", function () { resetKick("dzh"); });
    btnCone.addEventListener("click", function () { resetKick("cone"); });
    if (btnEllipsoid) {
      btnEllipsoid.addEventListener("click", function () {
        state.showEllipsoid = !state.showEllipsoid;
        btnEllipsoid.classList.toggle("active", state.showEllipsoid);
        render();
      });
    }
    if (btnLens) {
      btnLens.addEventListener("click", function () {
        state.showLens = !state.showLens;
        btnLens.classList.toggle("active", state.showLens);
        render();
      });
    }
    if (btnPause) {
      btnPause.addEventListener("click", function () {
        state.paused = !state.paused;
        btnPause.textContent = state.paused ? "▶ Resume" : "⏸ Pause";
        btnPause.classList.toggle("active", state.paused);
      });
    }

    window.MG_SIM2 = {
      load: function (o) {
        o = o || {};
        if (o.sq) { state.sqKey = String(o.sq); sqSelect.value = state.sqKey; }
        if (o.model) { state.model = o.model; modelSelect.value = o.model; syncTabs(); }
        if (o.lam !== undefined) setLam(o.lam, o.lam === 0.2 ? btnCube : (Math.abs(o.lam - 1 / Math.sqrt(17)) < 1e-6 ? btnIso : (o.lam === 1 ? btnOne : null)));
        state.paused = false;
        if (btnPause) { btnPause.textContent = "⏸ Pause"; btnPause.classList.remove("active"); }
        resetKick(o.kick || "dzh");
      },
      preset: function (name) {
        const iso = 1 / Math.sqrt(17);
        if (name === "dual-compare") this.load({ sq: "46", model: "compare", lam: iso, kick: "dzh" });
        else if (name === "shapes-gallery") this.load({ sq: "46", model: "gallery", lam: iso, kick: "dzh" });
        else if (name === "cube-twin") this.load({ sq: "46", model: "vs-cube", lam: iso, kick: "cone" });
        else if (name === "iso-top") this.load({ model: "point", lam: iso, kick: "tilt" });
        else if (name === "durer-calm") this.load({ sq: "175", model: "compare", lam: iso, kick: "dzh" });
      }
    };

    function frame() {
      if (isVisible("sim-precession")) {
        if (!state.paused) {
          const models = modelsActive();
          for (let s = 0; s < 2; s++) {
            models.forEach(function (m) {
              stepBody(state.bodies[m], momentsFor(m), 0.012);
            });
          }
        }
        render();
      }
      requestAnimationFrame(frame);
    }
    syncTabs();
    render();
    requestAnimationFrame(frame);
  }

  // =========================================================================
  // SIMULATOR 3: "Diamond-in-a-Diamond" Cutaway & Animated Seesaw Balance
  // =========================================================================
  function initSim3() {
    const sqSelect = document.getElementById("nest-sq-select");
    const rhoSlider = document.getElementById("nest-rho-slider");
    const rhoVal = document.getElementById("nest-rho-val");
    const peelSlider = document.getElementById("nest-peel-slider");
    const peelVal = document.getElementById("nest-peel-val");
    const btnSnap = document.getElementById("btn-snap-balance");
    const btnReset = document.getElementById("btn-reset-rho");
    const btnPeelAnim = document.getElementById("btn-nest-peel-anim");
    const btnLens = document.getElementById("btn-nest-lens");
    const canvas3d = document.getElementById("canvas-nest-3d");
    const canvasBal = document.getElementById("canvas-nest-balance");
    const readout = document.getElementById("nest-readout");
    if (!canvas3d || !canvasBal) return;

    const ctx3 = canvas3d.getContext("2d");
    const ctxB = canvasBal.getContext("2d");
    const cam = { yaw: -0.58, pitch: 0.38 };
    let dirty = true;
    attachOrbitControl(canvas3d, cam, function () { dirty = true; });
    watchVisibility("sim-nested");

    // Exact balancing ratios certified in anc/results_paper_c.json
    const EXACT_RATIOS = {
      "673": "5/4", "502": "4/3", "45": "85/61", "307": "23/15", "49": "2",
      "123": "-3/17", "54": "-57/58", "86": "0", "739": "0", "756": "0"
    };
    function parseFrac(s) {
      const p = s.split("/");
      return p.length === 2 ? parseFloat(p[0]) / parseFloat(p[1]) : parseFloat(s);
    }

    const state = {
      sqKey: sqSelect.value || "673",
      deltaRho: 0,
      peel: parseFloat(peelSlider.value) || 0.25,
      tiltCur: 0,
      showLens: true,
      rhoAnim: null,
      peelAnim: null
    };

    function getGem() { return GEMS[state.sqKey] || GEMS["673"]; }
    function axisOf(gem) {
      const sx = Math.abs(gem.c0[0]) + Math.abs(gem.c1[0]);
      const sy = Math.abs(gem.c0[1]) + Math.abs(gem.c1[1]);
      return sx > sy ? 0 : 1;
    }
    function composite(gem, d) {
      const den = gem.vol0 + d * gem.vol1;
      return [0, 1, 2].map(function (j) { return (gem.vol0 * gem.c0[j] + d * gem.vol1 * gem.c1[j]) / den; });
    }
    function isNatural(gem) { return Math.abs(gem.c0[0]) + Math.abs(gem.c0[1]) + Math.abs(gem.c0[2]) < 1e-12; }
    function balanceRatio(gem) {
      const key = String(gem.idx1);
      if (EXACT_RATIOS[key] !== undefined) return { val: parseFrac(EXACT_RATIOS[key]), label: EXACT_RATIOS[key] };
      const c1n = vecDot(gem.c1, gem.c1);
      if (gem.vol1 <= 0 || c1n < 1e-12) return { val: 0, label: "0" };
      const v = -(gem.vol0 * vecDot(gem.c0, gem.c1)) / (gem.vol1 * c1n);
      return { val: v, label: v.toFixed(3) };
    }
    // Square-root compression makes tiny imbalances visible without saturating big ones
    function targetTilt(c) {
      const a = Math.abs(c);
      if (a < 5e-5) return 0;
      return Math.sign(c) * Math.min(0.36, Math.sqrt(a) * 1.3);
    }

    function setRho(v, label) {
      state.deltaRho = v;
      rhoSlider.value = v.toFixed(2);
      rhoVal.textContent = label ? label + " (" + v.toFixed(3) + ")" : v.toFixed(2);
      dirty = true;
    }
    function setPeel(v) {
      state.peel = v;
      peelSlider.value = v.toFixed(2);
      peelVal.textContent = v.toFixed(2);
      dirty = true;
    }

    function render3D(gem, comp, ax) {
      const W = canvas3d.width, H = canvas3d.height;
      ctx3.clearRect(0, 0, W, H);
      const scale = 64, zS = 0.22;
      const pts = gem.P_real.map(function (p) { return [p[0], p[1], p[2] * zS]; });
      const P = function (pt) { return project3D(pt, cam, W, H, scale); };

      ctx3.fillStyle = "#132a2c";
      ctx3.font = "bold 12.5px -apple-system, sans-serif";
      ctx3.fillText("Gem #" + gem.idx1 + " · " + gem.vertices0.length + " outer vertices ⊃ " + gem.inner_idx.length + " trapped inner points", 14, 20);

      // Symmetry / balance axis
      const axv = ax === 0 ? [1, 0, 0] : [0, 1, 0];
      const a1 = P(vecScale(axv, -3.2)), a2 = P(vecScale(axv, 3.2));
      ctx3.save();
      ctx3.strokeStyle = "rgba(92, 105, 109, 0.55)";
      ctx3.setLineDash([4, 4]);
      ctx3.beginPath(); ctx3.moveTo(a1.x, a1.y); ctx3.lineTo(a2.x, a2.y); ctx3.stroke();
      ctx3.restore();

      // Inner core: color encodes density (deep gold = denser, pale dashed = lighter/hollow)
      const rho1 = 1 + state.deltaRho;
      const lighter = state.deltaRho < -0.01;
      const coreAlpha = Math.max(0.1, Math.min(0.92, 0.25 + 0.3 * rho1));
      if (gem.rk1 === 3 && gem.faces1 && gem.faces1.length) {
        const fl = gem.faces1.map(function (tri) {
          const tp = tri.map(function (vi) { return pts[vi]; });
          let c = [0, 0, 0];
          tp.forEach(function (p) { c = vecAdd(c, p); });
          return { tp: tp, d: P(vecScale(c, 1 / tp.length)).depth };
        }).sort(function (a, b) { return a.d - b.d; });
        fl.forEach(function (f) {
          ctx3.save();
          ctx3.fillStyle = lighter ? "rgba(253, 230, 138," + coreAlpha.toFixed(2) + ")" : "rgba(217, 119, 6," + coreAlpha.toFixed(2) + ")";
          ctx3.strokeStyle = "#92400e";
          ctx3.lineWidth = 1.3;
          if (lighter) ctx3.setLineDash([3, 3]);
          ctx3.beginPath();
          f.tp.forEach(function (p, i) { const q = P(p); if (i === 0) ctx3.moveTo(q.x, q.y); else ctx3.lineTo(q.x, q.y); });
          ctx3.closePath();
          ctx3.fill();
          ctx3.stroke();
          ctx3.restore();
        });
      } else if (gem.inner_idx.length > 1) {
        const ip = gem.inner_idx.map(function (vi) { return pts[vi]; });
        let c = [0, 0, 0];
        ip.forEach(function (p) { c = vecAdd(c, p); });
        c = vecScale(c, 1 / ip.length);
        ip.sort(function (a, b) { return Math.atan2(a[1] - c[1], a[0] - c[0]) - Math.atan2(b[1] - c[1], b[0] - c[0]); });
        ctx3.fillStyle = "rgba(217, 119, 6, 0.35)";
        ctx3.strokeStyle = "#d97706";
        ctx3.lineWidth = 2.2;
        ctx3.beginPath();
        ip.forEach(function (p, i) { const q = P(p); if (i === 0) ctx3.moveTo(q.x, q.y); else ctx3.lineTo(q.x, q.y); });
        ctx3.closePath();
        ctx3.fill();
        ctx3.stroke();
      }
      gem.inner_idx.forEach(function (vi) {
        const q = P(pts[vi]);
        ctx3.fillStyle = "#d97706";
        ctx3.beginPath(); ctx3.arc(q.x, q.y, 3.4, 0, Math.PI * 2); ctx3.fill();
      });

      // Outer hull, exploded outward by the peel amount
      const explode = state.peel * 0.6;
      const alpha = Math.max(0.04, 0.42 - state.peel * 0.42);
      const fo = gem.faces0.map(function (f) {
        const fp = f.verts.map(function (vi) { return pts[vi]; });
        let c = [0, 0, 0];
        fp.forEach(function (p) { c = vecAdd(c, p); });
        c = vecScale(c, 1 / fp.length);
        const shifted = fp.map(function (p) { return vecAdd(p, vecScale(c, explode)); });
        return { sp: shifted, d: P(c).depth };
      }).sort(function (a, b) { return a.d - b.d; });
      fo.forEach(function (f) {
        ctx3.fillStyle = "rgba(15, 118, 110," + alpha.toFixed(2) + ")";
        ctx3.strokeStyle = "rgba(15, 118, 110, 0.7)";
        ctx3.lineWidth = 1.1;
        ctx3.beginPath();
        f.sp.forEach(function (p, i) { const q = P(p); if (i === 0) ctx3.moveTo(q.x, q.y); else ctx3.lineTo(q.x, q.y); });
        ctx3.closePath();
        ctx3.fill();
        ctx3.stroke();
      });

      // Centroids: show both TRUE 1x position inside the gem and a magnified callout arrow so it never looks like c0/c1 is on the outer face
      const cmax = Math.max(vecNorm(gem.c0), vecNorm(gem.c1), 1e-6);
      const mag = Math.min(28, 0.85 / cmax);
      const truePt = function (c) { return [c[0], c[1], c[2] * zS]; };
      const sc = function (c) { return [c[0] * mag, c[1] * mag, c[2] * zS * mag]; };
      const pO = P([0, 0, 0]);
      ctx3.fillStyle = "#132a2c";
      ctx3.beginPath(); ctx3.arc(pO.x, pO.y, 4, 0, Math.PI * 2); ctx3.fill();
      ctx3.font = "bold 11px -apple-system, sans-serif";
      ctx3.fillText("O", pO.x - 14, pO.y + 4);
      if (vecNorm(gem.c0) > 1e-9) {
        const qTrue = P(truePt(gem.c0));
        const q = P(sc(gem.c0));
        ctx3.save();
        ctx3.strokeStyle = "rgba(15, 118, 110, 0.7)";
        ctx3.setLineDash([2, 2]);
        ctx3.beginPath(); ctx3.moveTo(qTrue.x, qTrue.y); ctx3.lineTo(q.x, q.y); ctx3.stroke();
        ctx3.restore();
        ctx3.fillStyle = "#0f766e";
        ctx3.beginPath(); ctx3.arc(qTrue.x, qTrue.y, 3.0, 0, Math.PI * 2); ctx3.fill();
        ctx3.beginPath(); ctx3.arc(q.x, q.y, 6.0, 0, Math.PI * 2); ctx3.fill();
        ctx3.fillText("c₀ (×" + mag.toFixed(0) + ")", q.x + 8, q.y - 5);
      }
      if (vecNorm(gem.c1) > 1e-9) {
        const qTrue = P(truePt(gem.c1));
        const q = P(sc(gem.c1));
        ctx3.save();
        ctx3.strokeStyle = "rgba(217, 119, 6, 0.7)";
        ctx3.setLineDash([2, 2]);
        ctx3.beginPath(); ctx3.moveTo(qTrue.x, qTrue.y); ctx3.lineTo(q.x, q.y); ctx3.stroke();
        ctx3.restore();
        ctx3.fillStyle = "#d97706";
        ctx3.beginPath(); ctx3.arc(qTrue.x, qTrue.y, 3.0, 0, Math.PI * 2); ctx3.fill();
        ctx3.beginPath();
        ctx3.moveTo(q.x, q.y - 6.5); ctx3.lineTo(q.x + 6.5, q.y); ctx3.lineTo(q.x, q.y + 6.5); ctx3.lineTo(q.x - 6.5, q.y);
        ctx3.closePath(); ctx3.fill();
        ctx3.fillText("c₁ (×" + mag.toFixed(0) + ")", q.x + 8, q.y + 11);
      }
      const balanced = vecNorm(comp) < 5e-4;
      const qcTrue = P(truePt(comp));
      const qc = P(sc(comp));
      ctx3.save();
      if (balanced) { ctx3.shadowColor = "#2dd4bf"; ctx3.shadowBlur = 14; }
      ctx3.fillStyle = balanced ? "#0f766e" : "#e11d48";
      ctx3.beginPath(); ctx3.arc(qcTrue.x, qcTrue.y, 3.2, 0, Math.PI * 2); ctx3.fill();
      ctx3.beginPath(); ctx3.arc(qc.x, qc.y, 5.2, 0, Math.PI * 2); ctx3.fill();
      ctx3.restore();

      ctx3.font = "11px -apple-system, sans-serif";
      ctx3.fillStyle = "#5c696d";
      ctx3.fillText("small dot = true CoM · large = ×" + mag.toFixed(0) + " zoom", W - 225, 38);
      ctx3.font = "bold 11.5px -apple-system, sans-serif";
      ctx3.fillStyle = "#0f766e";
      ctx3.fillText("■ Outer hull G₀ (vol " + gem.vol0_str + ")", 14, H - 26);
      ctx3.fillStyle = "#b45309";
      ctx3.fillText("◆ Inner core G₁ (vol " + gem.vol1_str + ", density ρ₁/ρ₀ = " + rho1.toFixed(2) + ")", 14, H - 9);

      if (state.showLens) {
        const innerMap = {};
        gem.inner_idx.forEach(function (vi) { innerMap[vi] = true; });
        drawSquareLensHUD(ctx3, gem.S, {
          show: true,
          mode: "nested",
          innerSet: innerMap,
          title: "#" + gem.idx1 + " (V₀=" + gem.vertices0.length + ", V₁=" + gem.inner_idx.length + ")",
          x: 10,
          y: 30,
          cellSz: 19
        });
      }
    }

    function renderBalance(gem, comp, ax) {
      const WB = canvasBal.width, HB = canvasBal.height;
      ctxB.clearRect(0, 0, WB, HB);
      const axName = ax === 0 ? "x" : "y";
      ctxB.fillStyle = "#132a2c";
      ctxB.font = "bold 12.5px -apple-system, sans-serif";
      ctxB.fillText("Seesaw along the " + axName + "-axis: outer shell vs. inner core", 14, 20);

      const fulX = WB / 2, fulY = 122;
      const c0a = gem.c0[ax], c1a = gem.c1[ax];
      const m0 = gem.vol0, m1 = state.deltaRho * gem.vol1;
      const span = Math.max(Math.abs(c0a), Math.abs(c1a), 1e-9);
      const k = 165 / span;
      const balanced = Math.abs(comp[ax]) < 5e-4 && vecNorm(comp) < 5e-4;

      // Ground + fulcrum
      ctxB.fillStyle = "#e6ece9";
      ctxB.fillRect(fulX - 120, fulY + 34, 240, 6);
      ctxB.fillStyle = "#2c3a37";
      ctxB.beginPath(); ctxB.moveTo(fulX, fulY + 3); ctxB.lineTo(fulX - 20, fulY + 36); ctxB.lineTo(fulX + 20, fulY + 36); ctxB.closePath(); ctxB.fill();

      ctxB.save();
      ctxB.translate(fulX, fulY);
      ctxB.rotate(state.tiltCur);
      ctxB.fillStyle = balanced ? "#0f766e" : "#7c6a4a";
      ctxB.fillRect(-200, -4, 400, 7);
      ctxB.fillStyle = "#ffffff";
      ctxB.fillRect(-1, -4, 2, 7);
      // Shell mass at c0
      const r0 = 17;
      const x0 = c0a * k;
      ctxB.fillStyle = "rgba(15, 118, 110, 0.85)";
      ctxB.beginPath(); ctxB.arc(x0, -4 - r0, r0, 0, Math.PI * 2); ctxB.fill();
      ctxB.fillStyle = "#ffffff";
      ctxB.font = "bold 10px -apple-system, sans-serif";
      ctxB.textAlign = "center";
      ctxB.fillText("shell", x0, -4 - r0 + 3);
      // Core excess mass at c1 (dashed outline if negative = lighter / hollow)
      if (gem.vol1 > 0 && Math.abs(c1a) > 1e-9) {
        const x1 = c1a * k;
        const r1 = Math.max(4, Math.min(24, r0 * Math.sqrt(Math.abs(m1) / m0) * 2.2));
        ctxB.save();
        if (m1 >= 0) {
          ctxB.fillStyle = "rgba(217, 119, 6, 0.9)";
          ctxB.beginPath(); ctxB.arc(x1, -4 - r1, r1, 0, Math.PI * 2); ctxB.fill();
        } else {
          ctxB.strokeStyle = "#d97706";
          ctxB.lineWidth = 2;
          ctxB.setLineDash([4, 3]);
          ctxB.beginPath(); ctxB.arc(x1, -4 - r1, r1, 0, Math.PI * 2); ctxB.stroke();
        }
        ctxB.restore();
        ctxB.fillStyle = "#92400e";
        ctxB.fillText(m1 > 1e-6 ? "denser core +" : (m1 < -1e-6 ? "lighter core −" : "core (uniform)"), x1, -12 - 2 * r1);
      }
      ctxB.restore();
      ctxB.textAlign = "left";

      // Plumb line from the composite centre of mass
      const xc = comp[ax] * k;
      const px = fulX + xc * Math.cos(state.tiltCur), py = fulY + xc * Math.sin(state.tiltCur);
      ctxB.save();
      ctxB.strokeStyle = balanced ? "#0f766e" : "#e11d48";
      ctxB.setLineDash([3, 3]);
      ctxB.beginPath(); ctxB.moveTo(px, py); ctxB.lineTo(px, fulY + 60); ctxB.stroke();
      ctxB.restore();
      ctxB.fillStyle = balanced ? "#0f766e" : "#e11d48";
      ctxB.beginPath(); ctxB.arc(px, py, 5, 0, Math.PI * 2); ctxB.fill();
      ctxB.font = "bold 12.5px -apple-system, sans-serif";
      ctxB.textAlign = "center";
      ctxB.fillText(
        balanced ? "✓ Level: centre of mass exactly at O" : "Tips " + (comp[ax] > 0 ? "right" : "left") + " (centre of mass off O)",
        fulX, fulY + 62
      );
      ctxB.textAlign = "left";

      // Curve: composite centroid vs. core density
      const padL = 52, padR = 20, botY = 222, botH = 172;
      const dMin = -1, dMax = 2.5;
      const xOf = function (d) { return padL + ((d - dMin) / (dMax - dMin)) * (WB - padL - padR); };
      const samples = [];
      let maxAbs = 1e-6;
      for (let s = 0; s <= 140; s++) {
        const d = dMin + (dMax - dMin) * s / 140;
        const c = composite(gem, d)[ax];
        samples.push([d, c]);
        if (Math.abs(c) > maxAbs) maxAbs = Math.abs(c);
      }
      maxAbs *= 1.1;
      const zeroY = botY + botH / 2;
      const yOf = function (c) { return zeroY - (c / maxAbs) * (botH * 0.45); };

      ctxB.strokeStyle = "#cbd5d0";
      ctxB.strokeRect(padL, botY, WB - padL - padR, botH);
      ctxB.save();
      ctxB.strokeStyle = "#0f766e";
      ctxB.setLineDash([4, 4]);
      ctxB.beginPath(); ctxB.moveTo(padL, zeroY); ctxB.lineTo(WB - padR, zeroY); ctxB.stroke();
      ctxB.strokeStyle = "#c2ccc6";
      ctxB.beginPath(); ctxB.moveTo(xOf(0), botY); ctxB.lineTo(xOf(0), botY + botH); ctxB.stroke();
      ctxB.restore();
      ctxB.fillStyle = "#5c696d";
      ctxB.font = "10px -apple-system, sans-serif";
      [-1, 0, 1, 2].forEach(function (t) { ctxB.fillText(String(t), xOf(t) - 3, botY + botH + 12); });
      ctxB.fillText("balance", padL + 4, zeroY - 4);

      ctxB.strokeStyle = "#132a2c";
      ctxB.lineWidth = 2.2;
      ctxB.beginPath();
      samples.forEach(function (s, i) { if (i === 0) ctxB.moveTo(xOf(s[0]), yOf(s[1])); else ctxB.lineTo(xOf(s[0]), yOf(s[1])); });
      ctxB.stroke();
      ctxB.lineWidth = 1;

      const br = balanceRatio(gem);
      if (isNatural(gem)) {
        ctxB.fillStyle = "#0f766e";
        ctxB.font = "bold 11px -apple-system, sans-serif";
        ctxB.fillText("Naturally balanced: c₀ = 0 for every density", padL + 10, botY + 16);
      } else if (br.val >= dMin && br.val <= dMax) {
        const bx = xOf(br.val);
        ctxB.save();
        ctxB.strokeStyle = "#d97706";
        ctxB.setLineDash([3, 3]);
        ctxB.beginPath(); ctxB.moveTo(bx, botY); ctxB.lineTo(bx, botY + botH); ctxB.stroke();
        ctxB.restore();
        ctxB.fillStyle = "#d97706";
        ctxB.beginPath(); ctxB.arc(bx, zeroY, 4.5, 0, Math.PI * 2); ctxB.fill();
        ctxB.font = "bold 11px -apple-system, sans-serif";
        ctxB.fillText("Δρ₁/ρ₀ = " + br.label, Math.min(bx + 6, WB - padR - 95), botY + 15);
      }
      ctxB.fillStyle = "#e11d48";
      ctxB.beginPath(); ctxB.arc(xOf(state.deltaRho), yOf(comp[ax]), 6, 0, Math.PI * 2); ctxB.fill();
      ctxB.fillStyle = "#3b4b48";
      ctxB.font = "11px -apple-system, sans-serif";
      ctxB.fillText("core excess density Δρ₁/ρ₀  (−1 = hollow, 0 = uniform)", padL + 40, HB - 6);
    }

    function updateReadout(gem, comp) {
      const fmt = function (v) { return (Math.abs(v) < 1e-9 ? 0 : v).toFixed(4); };
      const ok = vecNorm(comp) < 5e-4;
      readout.innerHTML =
        "<span>vol(G₀) = <span class='hl'>" + gem.vol0_str + "</span>, vol(G₁) = <span class='hl'>" + gem.vol1_str + "</span></span>" +
        "<span>Centre of mass = <span class='" + (ok ? "hl" : "warn") + "'>(" + fmt(comp[0]) + ", " + fmt(comp[1]) + ", " + fmt(comp[2]) + ")</span></span>" +
        "<span>Seesaw: <span class='" + (ok ? "hl" : "warn") + "'>" + (ok ? "LEVEL ✓" : (state.tiltCur * 180 / Math.PI).toFixed(1) + "° tilt") + "</span></span>";
    }

    function snap() {
      const gem = getGem();
      const br = balanceRatio(gem);
      const to = isNatural(gem) ? 0 : br.val;
      state.rhoAnim = { from: state.deltaRho, to: to, t0: performance.now(), dur: 1000, label: isNatural(gem) ? "0 (natural)" : br.label };
    }

    sqSelect.addEventListener("change", function () { state.sqKey = sqSelect.value; state.rhoAnim = null; setRho(0); });
    rhoSlider.addEventListener("input", function () { state.rhoAnim = null; setRho(parseFloat(rhoSlider.value)); });
    peelSlider.addEventListener("input", function () { state.peelAnim = null; setPeel(parseFloat(peelSlider.value)); });
    btnSnap.addEventListener("click", snap);
    btnReset.addEventListener("click", function () {
      state.rhoAnim = { from: state.deltaRho, to: 0, t0: performance.now(), dur: 700, label: null };
    });
    if (btnPeelAnim) {
      btnPeelAnim.addEventListener("click", function () {
        state.peelAnim = { from: state.peel, t0: performance.now(), dur: 2600 };
      });
    }
    if (btnLens) {
      btnLens.addEventListener("click", function () {
        state.showLens = !state.showLens;
        btnLens.classList.toggle("active", state.showLens);
        dirty = true;
      });
    }

    window.MG_SIM3 = {
      load: function (o) {
        o = o || {};
        if (o.sq) { state.sqKey = String(o.sq); sqSelect.value = state.sqKey; }
        state.rhoAnim = null;
        setRho(0);
        state.tiltCur = 0;
        if (o.snap) setTimeout(snap, 650);
        if (o.peel) state.peelAnim = { from: state.peel, t0: performance.now(), dur: 2600 };
      },
      preset: function (name) {
        if (name === "gem673") this.load({ sq: "673", snap: true });
        else if (name === "hollow54") this.load({ sq: "54", snap: true });
        else if (name === "nat86") this.load({ sq: "86", peel: true });
      }
    };

    function frame(now) {
      if (state.rhoAnim) {
        const a = state.rhoAnim;
        const t = Math.min(1, (now - a.t0) / a.dur);
        setRho(a.from + (a.to - a.from) * easeInOut(t), t >= 1 ? a.label : null);
        if (t >= 1) state.rhoAnim = null;
      }
      if (state.peelAnim) {
        const a = state.peelAnim;
        const t = Math.min(1, (now - a.t0) / a.dur);
        const v = t < 0.5 ? a.from + (0.9 - a.from) * easeInOut(t * 2) : 0.9 + (0.25 - 0.9) * easeInOut(t * 2 - 1);
        setPeel(v);
        if (t >= 1) state.peelAnim = null;
      }
      const gem = getGem();
      const comp = composite(gem, state.deltaRho);
      const ax = axisOf(gem);
      const tgt = targetTilt(comp[ax]);
      if (Math.abs(tgt - state.tiltCur) > 1e-4) {
        state.tiltCur += (tgt - state.tiltCur) * 0.1;
        dirty = true;
      }
      if (dirty && isVisible("sim-nested")) {
        render3D(gem, comp, ax);
        renderBalance(gem, comp, ax);
        updateReadout(gem, comp);
        dirty = false;
      }
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  // =========================================================================
  // SIMULATOR 4 ("Build It"): Ball-and-Rod Wireframes, Complete K16 Strut
  // Networks & Unfolded Papercraft Nets (Theorem 4.4 & Proposition 4.5)
  // =========================================================================
  function initSimFab() {
    const sqSelect = document.getElementById("fab-sq-select");
    const lamSelect = document.getElementById("fab-lam-select");
    const rhoLabel = document.getElementById("fab-param-label");
    const rhoSlider = document.getElementById("fab-param-slider");
    const rhoVal = document.getElementById("fab-param-val");
    const peelSlider = document.getElementById("fab-peel-slider");
    const peelVal = document.getElementById("fab-peel-val");
    const btnSnap = document.getElementById("btn-fab-snap");
    const btnReset = document.getElementById("btn-fab-reset");
    const btnPeelAnim = document.getElementById("btn-fab-spread-anim");
    const btnSvg = document.getElementById("btn-fab-svg");
    const btnLens = document.getElementById("btn-fab-lens");
    const fabTabs = Array.prototype.slice.call(document.querySelectorAll("#fab-mode-tabs .sim-tab"));
    const rightBtns = Array.prototype.slice.call(document.querySelectorAll("[data-fab-right]"));
    const canvas3d = document.getElementById("canvas-fab-3d");
    const canvasBal = document.getElementById("canvas-fab-right");
    const readout = document.getElementById("fab-readout");
    if (!canvas3d || !canvasBal) return;

    const ctx3 = canvas3d.getContext("2d");
    const ctxB = canvasBal.getContext("2d");
    const cam = { yaw: -0.58, pitch: 0.38 };
    let dirty = true;
    attachOrbitControl(canvas3d, cam, function () { dirty = true; });
    watchVisibility("sim-fab");

    const state = {
      sqKey: sqSelect.value || "673",
      lambda: lamSelect ? parseFloat(lamSelect.value) || 1.00 : 1.00,
      fab: "wireframe",    // "wireframe" | "k16"
      right: "seesaw",     // "seesaw" | "paper"
      param: 0,            // wireframe: (d₁/d₀)² · k16: strut weighting μ
      peel: parseFloat(peelSlider.value) || 0.15,
      tiltCur: 0,
      rhoAnim: null,
      peelAnim: null,
      showLens: true,
      hoverFace: null,
      hoverEdge: null
    };
    let hitFaces2D = [];
    let hitEdges2D = [];
    let hitFaces3D = [];
    let hitEdges3D = [];

    function getGem() { return GEMS[state.sqKey] || GEMS["673"]; }

    // ---------------------------------------------------------------------
    // Skeleton extraction: outer/inner hull edges, complete K16 network and
    // BFS papercraft unfolding at the active lift scale lambda
    // ---------------------------------------------------------------------
    function faceConvexHullCycle(verts, plane, P) {
      let nx = plane[0], ny = plane[1], nz = plane[2];
      const nm = Math.hypot(nx, ny, nz) || 1;
      nx /= nm; ny /= nm; nz /= nm;
      const p0 = P[verts[0]];
      if (nx * p0[0] + ny * p0[1] + nz * p0[2] < 0) {
        nx = -nx; ny = -ny; nz = -nz;
      }
      const tx = Math.abs(nx) < 0.9 ? 1 : 0;
      const ty = Math.abs(nx) < 0.9 ? 0 : 1;
      let e1x = ty * nz, e1y = -tx * nz, e1z = tx * ny - ty * nx;
      const e1m = Math.hypot(e1x, e1y, e1z) || 1;
      e1x /= e1m; e1y /= e1m; e1z /= e1m;
      const e2x = ny * e1z - nz * e1y, e2y = nz * e1x - nx * e1z, e2z = nx * e1y - ny * e1x;
      const pts2d = verts.map(function (vi) {
        const p = P[vi];
        return {
          vi: vi,
          u: p[0] * e1x + p[1] * e1y + p[2] * e1z,
          v: p[0] * e2x + p[1] * e2y + p[2] * e2z
        };
      });
      pts2d.sort(function (a, b) { return (a.u - b.u) || (a.v - b.v); });
      function cross2(o, a, b) {
        return (a.u - o.u) * (b.v - o.v) - (a.v - o.v) * (b.u - o.u);
      }
      const lower = [];
      pts2d.forEach(function (p) {
        while (lower.length >= 2 && cross2(lower[lower.length - 2], lower[lower.length - 1], p) <= 1e-9) {
          lower.pop();
        }
        lower.push(p);
      });
      const upper = [];
      for (let i = pts2d.length - 1; i >= 0; i--) {
        const p = pts2d[i];
        while (upper.length >= 2 && cross2(upper[upper.length - 2], upper[upper.length - 1], p) <= 1e-9) {
          upper.pop();
        }
        upper.push(p);
      }
      upper.pop();
      lower.pop();
      return lower.concat(upper).map(function (p) { return p.vi; });
    }

    // Extract unique outer edges E(G_0) and inner edges E(G_1) at lift scale lam
    const edgeCache = {};
    function getGemSkeletons(sqKey, gem, lam) {
      const cacheKey = sqKey + "_" + lam.toFixed(2);
      if (edgeCache[cacheKey]) return edgeCache[cacheKey];
      const P1 = gem.P_real;
      const P = P1.map(function (p) { return [p[0], p[1], p[2] * lam]; });
      const e0Map = {};
      const edges0 = [];
      const cycFaces0 = gem.faces0.map(function (f) {
        return faceConvexHullCycle(f.verts, f.plane, P1);
      });
      cycFaces0.forEach(function (vs) {
        for (let i = 0; i < vs.length; i++) {
          const u = vs[i], v = vs[(i + 1) % vs.length];
          const a = Math.min(u, v), b = Math.max(u, v);
          const key = a + "_" + b;
          if (!e0Map[key]) {
            e0Map[key] = true;
            edges0.push([a, b]);
          }
        }
      });

      const e1Map = {};
      const edges1 = [];
      if (gem.rk1 === 3 && gem.faces1 && gem.faces1.length > 0) {
        const edgeTris = {};
        gem.faces1.forEach(function (tri) {
          const p0 = P[tri[0]], p1 = P[tri[1]], p2 = P[tri[2]];
          let nx = (p1[1] - p0[1]) * (p2[2] - p0[2]) - (p1[2] - p0[2]) * (p2[1] - p0[1]);
          let ny = (p1[2] - p0[2]) * (p2[0] - p0[0]) - (p1[0] - p0[0]) * (p2[2] - p0[2]);
          let nz = (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p1[1] - p0[1]) * (p2[0] - p0[0]);
          const nm = Math.hypot(nx, ny, nz) || 1;
          nx /= nm; ny /= nm; nz /= nm;
          for (let i = 0; i < 3; i++) {
            const u = tri[i], v = tri[(i + 1) % 3];
            const a = Math.min(u, v), b = Math.max(u, v);
            const key = a + "_" + b;
            if (!edgeTris[key]) edgeTris[key] = [];
            edgeTris[key].push([nx, ny, nz, a, b]);
          }
        });
        Object.keys(edgeTris).forEach(function (key) {
          const list = edgeTris[key];
          const dot = list.length >= 2
            ? Math.abs(list[0][0] * list[1][0] + list[0][1] * list[1][1] + list[0][2] * list[1][2])
            : 0;
          if (list.length === 1 || dot < 1 - 1e-6) {
            e1Map[key] = true;
            edges1.push([list[0][3], list[0][4]]);
          }
        });
      } else if (gem.inner_idx && gem.inner_idx.length >= 2) {
        // 2D or 1D inner core convex hull
        const inVerts = gem.inner_idx;
        const p0 = P[inVerts[0]], p1 = P[inVerts[1]];
        let nrm = [0, 0, 1];
        for (let k = 2; k < inVerts.length; k++) {
          const pk = P[inVerts[k]];
          const cx = (p1[1] - p0[1]) * (pk[2] - p0[2]) - (p1[2] - p0[2]) * (pk[1] - p0[1]);
          const cy = (p1[2] - p0[2]) * (pk[0] - p0[0]) - (p1[0] - p0[0]) * (pk[2] - p0[2]);
          const cz = (p1[0] - p0[0]) * (pk[1] - p0[1]) - (p1[1] - p0[1]) * (pk[0] - p0[0]);
          if (Math.hypot(cx, cy, cz) > 1e-6) {
            nrm = [cx, cy, cz];
            break;
          }
        }
        const cyc1 = faceConvexHullCycle(inVerts, [nrm[0], nrm[1], nrm[2], 0], P);
        for (let i = 0; i < cyc1.length; i++) {
          const u = cyc1[i], v = cyc1[(i + 1) % cyc1.length];
          const a = Math.min(u, v), b = Math.max(u, v);
          const key = a + "_" + b;
          if (!e1Map[key]) {
            e1Map[key] = true;
            edges1.push([a, b]);
          }
        }
      }

      function edgeStats(edgeList) {
        let L = 0;
        let mx = 0, my = 0, mz = 0;
        edgeList.forEach(function (e) {
          const p = P[e[0]], q = P[e[1]];
          const len = Math.hypot(p[0] - q[0], p[1] - q[1], p[2] - q[2]);
          L += len;
          mx += len * 0.5 * (p[0] + q[0]);
          my += len * 0.5 * (p[1] + q[1]);
          mz += len * 0.5 * (p[2] + q[2]);
        });
        const c = L > 1e-12 ? [mx / L, my / L, mz / L] : [0, 0, 0];
        return { L: L, c: c, m: [mx, my, mz] };
      }

      const st0 = edgeStats(edges0);
      const st1 = edgeStats(edges1);

      // Complete K_16 edges (all 120 pairs)
      const edgesK16 = [];
      for (let i = 0; i < 16; i++) {
        for (let j = i + 1; j < 16; j++) {
          const key = i + "_" + j;
          const kind = e0Map[key] ? "outer" : (e1Map[key] ? "inner" : "internal");
          edgesK16.push({ u: i, v: j, kind: kind });
        }
      }
      const stK16 = edgeStats(edgesK16.map(function (o) { return [o.u, o.v]; }));

      // Exact wireframe balance ratio rho_lin,1 / rho_lin,0 when c0_wire and c1_wire are strictly anti-parallel in 3D
      let wireRatio = 0.0;
      const n0w = Math.hypot(st0.c[0], st0.c[1], st0.c[2]);
      const n1w = Math.hypot(st1.c[0], st1.c[1], st1.c[2]);
      if (n0w > 1e-9 && n1w > 1e-9) {
        const crx = st0.c[1] * st1.c[2] - st0.c[2] * st1.c[1];
        const cry = st0.c[2] * st1.c[0] - st0.c[0] * st1.c[2];
        const crz = st0.c[0] * st1.c[1] - st0.c[1] * st1.c[0];
        const sinTheta = Math.hypot(crx, cry, crz) / (n0w * n1w);
        const dot01 = st0.c[0] * st1.c[0] + st0.c[1] * st1.c[1] + st0.c[2] * st1.c[2];
        if (sinTheta < 1e-6 && dot01 < 0) {
          wireRatio = -(st0.L * dot01) / (st1.L * n1w * n1w);
        }
      }

      // Compute 2D BFS Spanning-Tree Papercraft Unfolding of G_0(S) at active lift scale lam
      const Ppap = P;
      const F0 = cycFaces0.map(function (vs) { return vs.slice(); });
      const nF = F0.length;

      // Orient each face CCW wrt outward normal (away from origin)
      const normals = [];
      for (let fi = 0; fi < nF; fi++) {
        const vs = F0[fi];
        const p0 = Ppap[vs[0]], p1 = Ppap[vs[1]], p2 = Ppap[vs[2]];
        let nx = (p1[1] - p0[1]) * (p2[2] - p0[2]) - (p1[2] - p0[2]) * (p2[1] - p0[1]);
        let ny = (p1[2] - p0[2]) * (p2[0] - p0[0]) - (p1[0] - p0[0]) * (p2[2] - p0[2]);
        let nz = (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p1[1] - p0[1]) * (p2[0] - p0[0]);
        const nm = Math.hypot(nx, ny, nz) || 1;
        nx /= nm; ny /= nm; nz /= nm;
        if (nx * p0[0] + ny * p0[1] + nz * p0[2] < 0) {
          F0[fi].reverse();
          nx = -nx; ny = -ny; nz = -nz;
        }
        normals.push([nx, ny, nz]);
      }

      // Map undirected edge to incident faces
      const edgeToFaces = {};
      for (let fi = 0; fi < nF; fi++) {
        const vs = F0[fi];
        for (let k = 0; k < vs.length; k++) {
          const u = vs[k], v = vs[(k + 1) % vs.length];
          const key = Math.min(u, v) + "_" + Math.max(u, v);
          if (!edgeToFaces[key]) edgeToFaces[key] = [];
          edgeToFaces[key].push({ fi: fi, u: u, v: v });
        }
      }

      // Local 2D frame and polygon area for each face
      const frames = [];
      for (let fi = 0; fi < nF; fi++) {
        const vs = F0[fi];
        const p0 = Ppap[vs[0]], p1 = Ppap[vs[1]];
        let e1x = p1[0] - p0[0], e1y = p1[1] - p0[1], e1z = p1[2] - p0[2];
        const L1 = Math.hypot(e1x, e1y, e1z) || 1;
        e1x /= L1; e1y /= L1; e1z /= L1;
        const n = normals[fi];
        const e2x = n[1] * e1z - n[2] * e1y;
        const e2y = n[2] * e1x - n[0] * e1z;
        const e2z = n[0] * e1y - n[1] * e1x;
        const localPts = {};
        const polyArr = [];
        vs.forEach(function (vi) {
          const d = [Ppap[vi][0] - p0[0], Ppap[vi][1] - p0[1], Ppap[vi][2] - p0[2]];
          const uv = [d[0] * e1x + d[1] * e1y + d[2] * e1z, d[0] * e2x + d[1] * e2y + d[2] * e2z];
          localPts[vi] = uv;
          polyArr.push(uv);
        });
        let area2 = 0;
        for (let i = 0; i < polyArr.length; i++) {
          const j = (i + 1) % polyArr.length;
          area2 += polyArr[i][0] * polyArr[j][1] - polyArr[j][0] * polyArr[i][1];
        }
        frames.push({ localPts: localPts, area: 0.5 * Math.abs(area2) });
      }

      // Separating-axis 2D polygon overlap test (strict interior overlap)
      function polysOverlap2D(p1, p2) {
        const eps = 1e-4;
        const list = [p1, p2];
        for (let pIdx = 0; pIdx < 2; pIdx++) {
          const poly = list[pIdx];
          const m = poly.length;
          for (let i = 0; i < m; i++) {
            const ex = poly[(i + 1) % m].x - poly[i].x;
            const ey = poly[(i + 1) % m].y - poly[i].y;
            const nm = Math.hypot(ex, ey);
            if (nm < 1e-12) continue;
            const ax = -ey / nm, ay = ex / nm;
            let min1 = Infinity, max1 = -Infinity, min2 = Infinity, max2 = -Infinity;
            for (let k = 0; k < p1.length; k++) {
              const v = p1[k].x * ax + p1[k].y * ay;
              if (v < min1) min1 = v;
              if (v > max1) max1 = v;
            }
            for (let k = 0; k < p2.length; k++) {
              const v = p2[k].x * ax + p2[k].y * ay;
              if (v < min2) min2 = v;
              if (v > max2) max2 = v;
            }
            if (max1 <= min2 + eps || max2 <= min1 + eps) return false;
          }
        }
        return true;
      }

      // Candidate roots sorted by descending facet area (matching verify_paper_c.py)
      const rootOrder = [];
      for (let fi = 0; fi < nF; fi++) rootOrder.push(fi);
      rootOrder.sort(function (a, b) { return frames[b].area - frames[a].area; });

      function buildBfsNet(rootIdx) {
        const visited = {};
        visited[rootIdx] = true;
        const globalPolys = {};
        globalPolys[rootIdx] = F0[rootIdx].map(function (vi) {
          return { vi: vi, x: frames[rootIdx].localPts[vi][0], y: frames[rootIdx].localPts[vi][1] };
        });
        const foldEdges = [];
        const treeKeys = [];
        const treeMap = {};
        const queue = [rootIdx];
        let overlaps = 0;

        while (queue.length > 0) {
          const fCurr = queue.shift();
          const vs = F0[fCurr];
          for (let k = 0; k < vs.length; k++) {
            const u = vs[k], v = vs[(k + 1) % vs.length];
            const key = Math.min(u, v) + "_" + Math.max(u, v);
            const inc = edgeToFaces[key] || [];
            inc.forEach(function (item) {
              const fNext = item.fi;
              if (visited[fNext]) return;
              visited[fNext] = true;
              treeMap[key] = true;
              treeKeys.push(key);
              queue.push(fNext);

              const polyCurr = globalPolys[fCurr];
              let Gu = null, Gv = null;
              polyCurr.forEach(function (pt) {
                if (pt.vi === u) Gu = [pt.x, pt.y];
                if (pt.vi === v) Gv = [pt.x, pt.y];
              });
              const Lu = frames[fNext].localPts[u];
              const Lv = frames[fNext].localPts[v];
              const dG = [Gu[0] - Gv[0], Gu[1] - Gv[1]];
              const dL = [Lu[0] - Lv[0], Lu[1] - Lv[1]];
              const ang = Math.atan2(dG[1], dG[0]) - Math.atan2(dL[1], dL[0]);
              const ca = Math.cos(ang), sa = Math.sin(ang);
              const nextPoly = F0[fNext].map(function (vi) {
                const lp = frames[fNext].localPts[vi];
                const dx = lp[0] - Lv[0], dy = lp[1] - Lv[1];
                return {
                  vi: vi,
                  x: Gv[0] + ca * dx - sa * dy,
                  y: Gv[1] + sa * dx + ca * dy
                };
              });
              Object.keys(globalPolys).forEach(function (prevKey) {
                if (polysOverlap2D(nextPoly, globalPolys[prevKey])) overlaps++;
              });
              globalPolys[fNext] = nextPoly;
              foldEdges.push({ seg: [Gu, Gv], key: key, f0: fCurr, f1: fNext });
            });
          }
        }
        return { rootIdx: rootIdx, globalPolys: globalPolys, foldEdges: foldEdges, treeKeys: treeMap, overlaps: overlaps };
      }

      let bestNet = null;
      for (let rIdx = 0; rIdx < rootOrder.length; rIdx++) {
        const cand = buildBfsNet(rootOrder[rIdx]);
        if (!bestNet || cand.overlaps < bestNet.overlaps) {
          bestNet = cand;
        }
        if (cand.overlaps === 0) break;
      }
      const globalPolys = bestNet.globalPolys;
      const foldEdges = bestNet.foldEdges;
      const treeKeys = bestNet.treeKeys;

      // Point-in-polygon check so glue tabs never overlap an unfolded facet
      function pointInPoly2D(px, py, poly) {
        let inside = false;
        for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
          const xi = poly[i].x, yi = poly[i].y;
          const xj = poly[j].x, yj = poly[j].y;
          const intersect = ((yi > py) !== (yj > py)) && (px < (xj - xi) * (py - yi) / ((yj - yi) || 1e-12) + xi);
          if (intersect) inside = !inside;
        }
        return inside;
      }

      const cutEdges = [];
      const glueTabs = [];
      let tabLetterIdx = 0;
      const sortedCutKeys = Object.keys(edgeToFaces).filter(function (k) { return !treeKeys[k]; }).sort();
      sortedCutKeys.forEach(function (key) {
        const letter = String.fromCharCode(97 + (tabLetterIdx % 26));
        tabLetterIdx++;
        const inc = edgeToFaces[key];
        const candidates = [];
        inc.forEach(function (item, idx) {
          const poly = globalPolys[item.fi];
          if (!poly) return;
          let A = null, B = null, cx = 0, cy = 0;
          poly.forEach(function (pt) {
            cx += pt.x; cy += pt.y;
            if (pt.vi === item.u) A = [pt.x, pt.y];
            if (pt.vi === item.v) B = [pt.x, pt.y];
          });
          cx /= poly.length; cy /= poly.length;

          const tVec = [B[0] - A[0], B[1] - A[1]];
          const eLen = Math.hypot(tVec[0], tVec[1]) || 1;
          const tHat = [tVec[0] / eLen, tVec[1] / eLen];
          let nOut = [tHat[1], -tHat[0]];
          const mid = [0.5 * (A[0] + B[0]), 0.5 * (A[1] + B[1])];
          if (nOut[0] * (mid[0] - cx) + nOut[1] * (mid[1] - cy) < 0) {
            nOut = [-nOut[0], -nOut[1]];
          }
          const hTab = Math.min(0.22, 0.17 * eLen);
          const inset = 0.18 * eLen;
          const T1 = [A[0] + inset * tHat[0] + hTab * nOut[0], A[1] + inset * tHat[1] + hTab * nOut[1]];
          const T2 = [B[0] - inset * tHat[0] + hTab * nOut[0], B[1] - inset * tHat[1] + hTab * nOut[1]];
          const probe = [mid[0] + 0.6 * hTab * nOut[0], mid[1] + 0.6 * hTab * nOut[1]];
          const lblPos = [mid[0] + 0.52 * hTab * nOut[0], mid[1] + 0.52 * hTab * nOut[1]];
          const partnerLblPos = [mid[0] - 0.12 * eLen * nOut[0], mid[1] - 0.12 * eLen * nOut[1]];
          let overlaps = false;
          Object.keys(globalPolys).forEach(function (fKey) {
            if (pointInPoly2D(probe[0], probe[1], globalPolys[fKey])) overlaps = true;
          });
          candidates.push({
            poly: [A, T1, T2, B],
            seg: [A, B],
            overlaps: overlaps,
            idx: idx,
            fi: item.fi,
            key: key,
            letter: letter,
            lblPos: lblPos,
            partnerLblPos: partnerLblPos
          });
        });
        if (candidates.length > 0) {
          const best = candidates.find(function (c) { return !c.overlaps; }) || candidates[0];
          glueTabs.push({
            poly: best.poly,
            key: key,
            letter: letter,
            lblPos: best.lblPos,
            fi: best.fi
          });
          candidates.forEach(function (c) {
            cutEdges.push({
              seg: c.seg,
              key: key,
              letter: letter,
              hasTab: c === best,
              partnerLblPos: c.partnerLblPos,
              fi: c.fi
            });
          });
        }
      });

      edgeCache[cacheKey] = {
        edges0: edges0,
        edges1: edges1,
        edgesK16: edgesK16,
        st0: st0,
        st1: st1,
        stK16: stK16,
        wireRatio: wireRatio,
        papercraft: {
          rootIdx: bestNet.rootIdx,
          F0: F0,
          polys: globalPolys,
          foldEdges: foldEdges,
          cutEdges: cutEdges,
          glueTabs: glueTabs,
          f0: gem.vertices0.length,
          f1: edges0.length,
          f2: nF
        }
      };
      return edgeCache[cacheKey];
    }

    function skel() { return getGemSkeletons(state.sqKey, getGem(), state.lambda); }

    function paramRange() {
      if (state.fab === "wireframe") {
        const wr = skel().wireRatio;
        return [0, wr > 2.0 ? Math.ceil(wr * 1.2) : 2.5];
      }
      return [0, 1];
    }

    function stats(p) {
      const sk = skel();
      if (state.fab === "wireframe") {
        const L0 = sk.st0.L, L1 = sk.st1.L, c0 = sk.st0.c, c1 = sk.st1.c;
        const den = L0 + p * L1;
        const comp = den > 1e-12 ? [0, 1, 2].map(function (j) { return (L0 * c0[j] + p * L1 * c1[j]) / den; }) : [0, 0, 0];
        return { m0: L0, m1: L1, c0: c0, c1: c1, comp: comp };
      }
      const mu = Math.max(0, Math.min(1, p));
      return { m0: sk.stK16.L, m1: 0, c0: sk.stK16.c, c1: [0, 0, 0], comp: vecScale(sk.stK16.c, mu) };
    }

    function axisOf(st) {
      const sx = Math.abs(st.c0[0]) + Math.abs(st.c1[0]);
      const sy = Math.abs(st.c0[1]) + Math.abs(st.c1[1]);
      return sx > sy ? 0 : 1;
    }

    // Balancing parameter for the current fabrication mode (null if none exists)
    function balanceTarget() {
      const sk = skel();
      if (state.fab === "wireframe") {
        if (sk.wireRatio > 0) return { val: sk.wireRatio, label: "d₁/d₀ = " + Math.sqrt(sk.wireRatio).toFixed(3) };
        if (vecNorm(sk.st0.c) < 1e-9 && vecNorm(sk.st1.c) < 1e-9) return { val: 0, label: "0 (natural)" };
        return null;
      }
      return { val: 0, label: "μ = 0 (equal-mass rods)" };
    }

    function fmtParam(v) {
      if (state.fab === "wireframe") return v.toFixed(2) + " (d₁/d₀ = " + Math.sqrt(Math.max(0, v)).toFixed(3) + ")";
      return v.toFixed(2);
    }
    function setParam(v, label) {
      state.param = v;
      rhoSlider.value = v.toFixed(3);
      rhoVal.textContent = label ? label : fmtParam(v);
      dirty = true;
    }
    function setPeel(v) {
      state.peel = v;
      peelSlider.value = v.toFixed(2);
      peelVal.textContent = v.toFixed(2);
      dirty = true;
    }

    function updateControls() {
      const r = paramRange();
      rhoSlider.min = r[0].toFixed(2);
      rhoSlider.max = r[1].toFixed(2);
      rhoSlider.step = r[1] - r[0] > 5 ? "0.05" : "0.01";
      const tgt = balanceTarget();
      if (state.fab === "wireframe") {
        rhoLabel.textContent = "Inner/Outer Rod Gauge (d₁/d₀)²:";
        btnSnap.textContent = tgt ? "Snap Rod Gauge (" + tgt.label + ")" : "No wireframe balance for this gem";
        btnReset.textContent = "Outer Rods Only (d₁ = 0)";
      } else {
        rhoLabel.textContent = "Strut Weighting μ (0 = equal mass, 1 = by length):";
        btnSnap.textContent = "Equal-Mass Rods (c = 0)";
        btnReset.textContent = "Constant-Gauge Rods (μ = 1)";
      }
      btnSnap.disabled = !tgt;
      btnSnap.style.opacity = tgt ? "1" : "0.5";
      if (lamSelect) lamSelect.value = state.lambda.toFixed(2);
      fabTabs.forEach(function (b) { b.classList.toggle("active", b.getAttribute("data-fab") === state.fab); });
      rightBtns.forEach(function (b) { b.classList.toggle("active", b.getAttribute("data-fab-right") === state.right); });
    }

    function targetTilt(c) {
      const a = Math.abs(c);
      if (a < 5e-5) return 0;
      return Math.sign(c) * Math.min(0.36, Math.sqrt(a) * 1.3);
    }

    // ------------------------------- 3D view -------------------------------
    function render3D(gem, st, ax) {
      const W = canvas3d.width, H = canvas3d.height;
      ctx3.clearRect(0, 0, W, H);
      const zS = state.lambda;
      const scale = state.lambda < 0.5 ? 64 : 26;
      const sk = skel();
      const pts = gem.P_real.map(function (p) { return [p[0], p[1], p[2] * zS]; });
      const P = function (pt) { return project3D(pt, cam, W, H, scale); };
      const innerSet = {};
      gem.inner_idx.forEach(function (vi) { innerSet[vi] = true; });

      ctx3.fillStyle = "#132a2c";
      ctx3.font = "bold 12.5px -apple-system, sans-serif";
      const titles = {
        wireframe: "Gem #" + gem.idx1 + " (λ=" + state.lambda.toFixed(2) + ") · ball-and-rod wireframe (outer + inner rods)",
        k16: "Gem #" + gem.idx1 + " (λ=" + state.lambda.toFixed(2) + ") · all 120 rods of the complete K₁₆ network"
      };
      ctx3.fillText(titles[state.fab], 14, 20);

      // Balance axis
      const axv = ax === 0 ? [1, 0, 0] : [0, 1, 0];
      const a1 = P(vecScale(axv, -3.2)), a2 = P(vecScale(axv, 3.2));
      ctx3.save();
      ctx3.strokeStyle = "rgba(92, 105, 109, 0.5)";
      ctx3.setLineDash([4, 4]);
      ctx3.beginPath(); ctx3.moveTo(a1.x, a1.y); ctx3.lineTo(a2.x, a2.y); ctx3.stroke();
      ctx3.restore();

      const grow = state.fab === "wireframe" ? (1 + state.peel * 0.24) : 1.0;

      // Record 3D facet polygons for linked 2D <-> 3D hover and highlight active hovered facet
      hitFaces3D = [];
      if (sk.papercraft && sk.papercraft.F0) {
        sk.papercraft.F0.forEach(function (vs, fi) {
          const poly2 = vs.map(function (vi) {
            const p = P(vecScale(pts[vi], grow));
            return { x: p.x, y: p.y, depth: p.depth };
          });
          let dAvg = 0;
          poly2.forEach(function (q) { dAvg += q.depth; });
          dAvg /= (poly2.length || 1);
          hitFaces3D.push({ fi: String(fi), poly: poly2, depth: dAvg });
        });
        if (state.hoverFace !== null && sk.papercraft.F0[state.hoverFace]) {
          const hPoly = sk.papercraft.F0[state.hoverFace].map(function (vi) { return P(vecScale(pts[vi], grow)); });
          ctx3.save();
          ctx3.fillStyle = "rgba(250, 204, 21, 0.42)";
          ctx3.strokeStyle = "#d97706";
          ctx3.lineWidth = 2.6;
          ctx3.beginPath();
          hPoly.forEach(function (q, idx) {
            if (idx === 0) ctx3.moveTo(q.x, q.y);
            else ctx3.lineTo(q.x, q.y);
          });
          ctx3.closePath();
          ctx3.fill();
          ctx3.stroke();
          ctx3.restore();
        }
      }

      hitEdges3D = [];
      if (state.fab === "wireframe") {
        sk.edges0.forEach(function (e) {
          const key = Math.min(e[0], e[1]) + "_" + Math.max(e[0], e[1]);
          const a = P(vecScale(pts[e[0]], grow)), b = P(vecScale(pts[e[1]], grow));
          hitEdges3D.push({ key: key, a: a, b: b });
          const isHov = state.hoverEdge === key;
          ctx3.strokeStyle = isHov ? "#e11d48" : "rgba(15, 118, 110, 0.88)";
          ctx3.lineWidth = isHov ? 5.2 : 3.2;
          ctx3.beginPath(); ctx3.moveTo(a.x, a.y); ctx3.lineTo(b.x, b.y); ctx3.stroke();
        });
        const dRatio = Math.sqrt(Math.max(0, state.param));
        const innerLW = Math.max(1.2, Math.min(7.0, 3.2 * (dRatio > 0.05 ? dRatio : 0.65)));
        sk.edges1.forEach(function (e) {
          const a = P(pts[e[0]]), b = P(pts[e[1]]);
          ctx3.strokeStyle = dRatio > 0.02 ? "rgba(217, 119, 6, 0.95)" : "rgba(217, 119, 6, 0.3)";
          ctx3.lineWidth = innerLW;
          ctx3.beginPath(); ctx3.moveTo(a.x, a.y); ctx3.lineTo(b.x, b.y); ctx3.stroke();
        });
        for (let i = 0; i < 16; i++) {
          const inner = !!innerSet[i];
          const q = P(inner ? pts[i] : vecScale(pts[i], grow));
          ctx3.fillStyle = inner ? "#d97706" : "#0f766e";
          ctx3.strokeStyle = "#ffffff";
          ctx3.lineWidth = 1.1;
          ctx3.beginPath(); ctx3.arc(q.x, q.y, inner ? 5.2 : 4.6, 0, Math.PI * 2); ctx3.fill(); ctx3.stroke();
        }
      } else {
        const intAlpha = Math.max(0.1, 0.5 - state.peel * 0.42);
        sk.edgesK16.forEach(function (item) {
          const key = Math.min(item.u, item.v) + "_" + Math.max(item.u, item.v);
          const a = P(pts[item.u]), b = P(pts[item.v]);
          if (item.kind === "outer") hitEdges3D.push({ key: key, a: a, b: b });
          const isHov = state.hoverEdge === key;
          if (isHov) { ctx3.strokeStyle = "#e11d48"; ctx3.lineWidth = 5.0; }
          else if (item.kind === "internal") { ctx3.strokeStyle = "rgba(29, 78, 216," + intAlpha.toFixed(2) + ")"; ctx3.lineWidth = 1.05; }
          else if (item.kind === "outer") { ctx3.strokeStyle = "rgba(15, 118, 110, 0.86)"; ctx3.lineWidth = 2.4; }
          else { ctx3.strokeStyle = "rgba(217, 119, 6, 0.92)"; ctx3.lineWidth = 2.5; }
          ctx3.beginPath(); ctx3.moveTo(a.x, a.y); ctx3.lineTo(b.x, b.y); ctx3.stroke();
        });
        for (let i = 0; i < 16; i++) {
          const inner = !!innerSet[i];
          const q = P(pts[i]);
          const sz = inner ? 9.5 : 8.5;
          ctx3.fillStyle = inner ? "#e6960f" : "#0f766e";
          ctx3.strokeStyle = "#132a2c";
          ctx3.lineWidth = 1.1;
          ctx3.fillRect(q.x - sz / 2, q.y - sz / 2, sz, sz);
          ctx3.strokeRect(q.x - sz / 2, q.y - sz / 2, sz, sz);
        }
      }

      // Centroids: show both TRUE 1x position inside the gem and a magnified callout arrow so it never looks like c0/c1 sits on the outer face
      const cmax = Math.max(vecNorm(st.c0), vecNorm(st.c1), 1e-6);
      const mag = Math.min(28, 0.85 / cmax);
      const zVisRatio = zS / state.lambda;
      const truePt = function (c) { return [c[0], c[1], c[2] * zVisRatio]; };
      const sc = function (c) { return [c[0] * mag, c[1] * mag, c[2] * zVisRatio * mag]; };
      const pO = P([0, 0, 0]);
      ctx3.fillStyle = "#132a2c";
      ctx3.beginPath(); ctx3.arc(pO.x, pO.y, 4, 0, Math.PI * 2); ctx3.fill();
      ctx3.font = "bold 11px -apple-system, sans-serif";
      ctx3.fillText("O", pO.x - 14, pO.y + 4);
      const lbl0 = state.fab === "k16" ? "c_len" : "c₀";
      if (vecNorm(st.c0) > 1e-9) {
        const qTrue = P(truePt(st.c0));
        const q = P(sc(st.c0));
        ctx3.save();
        ctx3.strokeStyle = "rgba(15, 118, 110, 0.7)";
        ctx3.setLineDash([2, 2]);
        ctx3.beginPath(); ctx3.moveTo(qTrue.x, qTrue.y); ctx3.lineTo(q.x, q.y); ctx3.stroke();
        ctx3.restore();
        ctx3.fillStyle = "#0f766e";
        ctx3.beginPath(); ctx3.arc(qTrue.x, qTrue.y, 3.0, 0, Math.PI * 2); ctx3.fill();
        ctx3.beginPath(); ctx3.arc(q.x, q.y, 6.0, 0, Math.PI * 2); ctx3.fill();
        ctx3.fillText(lbl0 + " (×" + mag.toFixed(0) + ")", q.x + 8, q.y - 5);
      }
      if (vecNorm(st.c1) > 1e-9) {
        const qTrue = P(truePt(st.c1));
        const q = P(sc(st.c1));
        ctx3.save();
        ctx3.strokeStyle = "rgba(217, 119, 6, 0.7)";
        ctx3.setLineDash([2, 2]);
        ctx3.beginPath(); ctx3.moveTo(qTrue.x, qTrue.y); ctx3.lineTo(q.x, q.y); ctx3.stroke();
        ctx3.restore();
        ctx3.fillStyle = "#d97706";
        ctx3.beginPath(); ctx3.arc(qTrue.x, qTrue.y, 3.0, 0, Math.PI * 2); ctx3.fill();
        ctx3.beginPath();
        ctx3.moveTo(q.x, q.y - 6.5); ctx3.lineTo(q.x + 6.5, q.y); ctx3.lineTo(q.x, q.y + 6.5); ctx3.lineTo(q.x - 6.5, q.y);
        ctx3.closePath(); ctx3.fill();
        ctx3.fillText("c₁ (×" + mag.toFixed(0) + ")", q.x + 8, q.y + 11);
      }
      const balanced = vecNorm(st.comp) < 5e-4;
      const qcTrue = P(truePt(st.comp));
      const qc = P(sc(st.comp));
      ctx3.save();
      if (balanced) { ctx3.shadowColor = "#2dd4bf"; ctx3.shadowBlur = 14; }
      ctx3.fillStyle = balanced ? "#0f766e" : "#e11d48";
      ctx3.beginPath(); ctx3.arc(qcTrue.x, qcTrue.y, 3.2, 0, Math.PI * 2); ctx3.fill();
      ctx3.beginPath(); ctx3.arc(qc.x, qc.y, 5.2, 0, Math.PI * 2); ctx3.fill();
      ctx3.restore();
      ctx3.font = "11px -apple-system, sans-serif";
      ctx3.fillStyle = "#5c696d";
      ctx3.fillText("small dot = true CoM · large = ×" + mag.toFixed(0) + " zoom", W - 225, 38);

      ctx3.font = "bold 11.5px -apple-system, sans-serif";
      if (state.fab === "wireframe") {
        ctx3.fillStyle = "#0f766e";
        ctx3.fillText("● " + sk.edges0.length + " outer rods, total length " + sk.st0.L.toFixed(1), 14, H - 26);
        ctx3.fillStyle = "#b45309";
        ctx3.fillText("● " + sk.edges1.length + " inner rods, length " + sk.st1.L.toFixed(1) + " · d₁/d₀ = " + Math.sqrt(Math.max(0, state.param)).toFixed(3), 14, H - 9);
      } else {
        ctx3.fillStyle = "#0f766e";
        ctx3.fillText("■ 120 rods: " + sk.edges0.length + " hull + " + sk.edges1.length + " core + " + (120 - sk.edges0.length - sk.edges1.length) + " internal", 14, H - 26);
        ctx3.fillStyle = "#1d4ed8";
        ctx3.fillText("■ total length " + sk.stK16.L.toFixed(1) + " · equal-mass rods always balance (Thm 4.4)", 14, H - 9);
      }

      if (state.showLens) {
        const hoverVerts = {};
        if (state.hoverFace !== null && sk.papercraft && sk.papercraft.F0 && sk.papercraft.F0[state.hoverFace]) {
          sk.papercraft.F0[state.hoverFace].forEach(function (vi) { hoverVerts[vi] = true; });
        }
        if (state.hoverEdge !== null) {
          const parts = String(state.hoverEdge).split("_");
          if (parts.length === 2) {
            hoverVerts[parseInt(parts[0], 10)] = true;
            hoverVerts[parseInt(parts[1], 10)] = true;
          }
        }
        drawSquareLensHUD(ctx3, gem.S, {
          x: W - 118,
          y: 50,
          size: 104,
          mode: "hull",
          innerIdx: gem.inner_idx,
          hoverVerts: hoverVerts,
          title: "#" + gem.idx1 + " · " + (16 - gem.inner_idx.length) + "+" + gem.inner_idx.length
        });
      }
    }

    // ------------------------------ Seesaw view ------------------------------
    function renderSeesaw(gem, st, ax) {
      const WB = canvasBal.width, HB = canvasBal.height;
      ctxB.clearRect(0, 0, WB, HB);
      const axName = ax === 0 ? "x" : "y";
      const NAMES = {
        wireframe: ["outer rods", "inner rods", "outer rods vs. inner rods"],
        k16: ["120 rods", "", "the complete strut network"]
      }[state.fab];
      ctxB.fillStyle = "#132a2c";
      ctxB.font = "bold 12.5px -apple-system, sans-serif";
      ctxB.fillText("Seesaw along the " + axName + "-axis (λ=" + state.lambda.toFixed(2) + "): " + NAMES[2], 14, 20);

      const fulX = WB / 2, fulY = 122;
      const c0a = st.c0[ax], c1a = st.c1[ax];
      const balanced = vecNorm(st.comp) < 5e-4;

      ctxB.fillStyle = "#e6ece9";
      ctxB.fillRect(fulX - 120, fulY + 34, 240, 6);
      ctxB.fillStyle = "#2c3a37";
      ctxB.beginPath(); ctxB.moveTo(fulX, fulY + 3); ctxB.lineTo(fulX - 20, fulY + 36); ctxB.lineTo(fulX + 20, fulY + 36); ctxB.closePath(); ctxB.fill();

      const span = Math.max(Math.abs(c0a), Math.abs(c1a), 1e-9);
      const k = 165 / span;
      ctxB.save();
      ctxB.translate(fulX, fulY);
      ctxB.rotate(state.tiltCur);
      ctxB.fillStyle = balanced ? "#0f766e" : "#7c6a4a";
      ctxB.fillRect(-200, -4, 400, 7);
      ctxB.fillStyle = "#ffffff";
      ctxB.fillRect(-1, -4, 2, 7);
      ctxB.textAlign = "center";
      ctxB.font = "bold 10px -apple-system, sans-serif";
      if (state.fab === "k16") {
        // Single weight: the rod network sits at mu * c_len
        const xr = st.comp[ax] * k;
        ctxB.fillStyle = "rgba(29, 78, 216, 0.85)";
        ctxB.beginPath(); ctxB.arc(xr, -21, 17, 0, Math.PI * 2); ctxB.fill();
        ctxB.fillStyle = "#ffffff";
        ctxB.fillText("rods", xr, -18);
      } else {
        const r0 = 17, x0 = c0a * k;
        ctxB.fillStyle = "rgba(15, 118, 110, 0.85)";
        ctxB.beginPath(); ctxB.arc(x0, -4 - r0, r0, 0, Math.PI * 2); ctxB.fill();
        ctxB.fillStyle = "#ffffff";
        ctxB.fillText(NAMES[0].split(" ")[0], x0, -4 - r0 + 3);
        if (st.m1 > 0 && Math.abs(c1a) > 1e-9) {
          const m1 = state.param * st.m1;
          const x1 = c1a * k;
          const r1 = Math.max(4, Math.min(24, r0 * Math.sqrt(Math.abs(m1) / st.m0) * 2.2));
          ctxB.save();
          if (m1 >= 0) {
            ctxB.fillStyle = "rgba(217, 119, 6, 0.9)";
            ctxB.beginPath(); ctxB.arc(x1, -4 - r1, r1, 0, Math.PI * 2); ctxB.fill();
          } else {
            ctxB.strokeStyle = "#d97706";
            ctxB.lineWidth = 2;
            ctxB.setLineDash([4, 3]);
            ctxB.beginPath(); ctxB.arc(x1, -4 - r1, r1, 0, Math.PI * 2); ctxB.stroke();
          }
          ctxB.restore();
          ctxB.fillStyle = "#92400e";
          const tag = m1 > 1e-6 ? "inner rods" : "no inner rods";
          ctxB.fillText(tag, x1, -12 - 2 * r1);
        }
      }
      ctxB.restore();
      ctxB.textAlign = "left";

      const xc = st.comp[ax] * k;
      const px = fulX + xc * Math.cos(state.tiltCur), py = fulY + xc * Math.sin(state.tiltCur);
      ctxB.save();
      ctxB.strokeStyle = balanced ? "#0f766e" : "#e11d48";
      ctxB.setLineDash([3, 3]);
      ctxB.beginPath(); ctxB.moveTo(px, py); ctxB.lineTo(px, fulY + 60); ctxB.stroke();
      ctxB.restore();
      ctxB.fillStyle = balanced ? "#0f766e" : "#e11d48";
      ctxB.beginPath(); ctxB.arc(px, py, 5, 0, Math.PI * 2); ctxB.fill();
      ctxB.font = "bold 12.5px -apple-system, sans-serif";
      ctxB.textAlign = "center";
      ctxB.fillText(balanced ? "✓ Level: centre of mass exactly at O" : "Tips " + (st.comp[ax] > 0 ? "right" : "left") + " (centre of mass off O)", fulX, fulY + 62);
      ctxB.textAlign = "left";

      // Centroid vs. parameter curve
      const padL = 52, padR = 20, botY = 222, botH = 172;
      const r = paramRange();
      const xOf = function (d) { return padL + ((d - r[0]) / (r[1] - r[0])) * (WB - padL - padR); };
      const samples = [];
      let maxAbs = 1e-6;
      for (let s = 0; s <= 140; s++) {
        const d = r[0] + (r[1] - r[0]) * s / 140;
        const c = stats(d).comp[ax];
        samples.push([d, c]);
        if (Math.abs(c) > maxAbs) maxAbs = Math.abs(c);
      }
      maxAbs *= 1.1;
      const zeroY = botY + botH / 2;
      const yOf = function (c) { return zeroY - (c / maxAbs) * (botH * 0.45); };
      ctxB.strokeStyle = "#cbd5d0";
      ctxB.strokeRect(padL, botY, WB - padL - padR, botH);
      ctxB.save();
      ctxB.strokeStyle = "#0f766e";
      ctxB.setLineDash([4, 4]);
      ctxB.beginPath(); ctxB.moveTo(padL, zeroY); ctxB.lineTo(WB - padR, zeroY); ctxB.stroke();
      ctxB.restore();
      ctxB.fillStyle = "#5c696d";
      ctxB.font = "10px -apple-system, sans-serif";
      const stepT = Math.max(0.25, Math.ceil((r[1] - r[0]) / 5 * 4) / 4);
      for (let t = Math.ceil(r[0] / stepT) * stepT; t <= r[1] + 1e-9; t += stepT) {
        ctxB.fillText(String(Math.round(t * 100) / 100), xOf(t) - 4, botY + botH + 12);
      }
      ctxB.fillText("balance", padL + 4, zeroY - 4);
      ctxB.strokeStyle = "#132a2c";
      ctxB.lineWidth = 2.2;
      ctxB.beginPath();
      samples.forEach(function (s, i) { if (i === 0) ctxB.moveTo(xOf(s[0]), yOf(s[1])); else ctxB.lineTo(xOf(s[0]), yOf(s[1])); });
      ctxB.stroke();
      ctxB.lineWidth = 1;

      const tgt = balanceTarget();
      if (tgt && tgt.label.indexOf("natural") >= 0) {
        ctxB.fillStyle = "#0f766e";
        ctxB.font = "bold 11px -apple-system, sans-serif";
        ctxB.fillText("Naturally balanced at every setting", padL + 10, botY + 16);
      } else if (tgt && tgt.val >= r[0] && tgt.val <= r[1]) {
        const bx = xOf(tgt.val);
        ctxB.save();
        ctxB.strokeStyle = "#d97706";
        ctxB.setLineDash([3, 3]);
        ctxB.beginPath(); ctxB.moveTo(bx, botY); ctxB.lineTo(bx, botY + botH); ctxB.stroke();
        ctxB.restore();
        ctxB.fillStyle = "#d97706";
        ctxB.beginPath(); ctxB.arc(bx, zeroY, 4.5, 0, Math.PI * 2); ctxB.fill();
        ctxB.font = "bold 11px -apple-system, sans-serif";
        ctxB.fillText(tgt.label, Math.min(bx + 6, WB - padR - 150), botY + 15);
      } else if (!tgt) {
        ctxB.fillStyle = "#9f1239";
        ctxB.font = "bold 11px -apple-system, sans-serif";
        ctxB.fillText("c₀ and c₁ are not opposite: no setting balances this gem", padL + 10, botY + 16);
      }
      ctxB.fillStyle = "#e11d48";
      ctxB.beginPath(); ctxB.arc(xOf(state.param), yOf(st.comp[ax]), 6, 0, Math.PI * 2); ctxB.fill();
      ctxB.fillStyle = "#3b4b48";
      ctxB.font = "11px -apple-system, sans-serif";
      const xl = {
        wireframe: "inner/outer rod gauge (d₁/d₀)²  (0 = outer rods only)",
        k16: "strut weighting μ  (0 = equal-mass rods, 1 = constant-gauge rods)"
      }[state.fab];
      ctxB.fillText(xl, padL + 30, HB - 6);
    }

    // --------------------------- Papercraft net view ---------------------------
    function renderPapercraft(gem, sk) {
      const WB = canvasBal.width, HB = canvasBal.height;
      ctxB.clearRect(0, 0, WB, HB);
      const net = sk.papercraft;
      ctxB.fillStyle = "#132a2c";
      ctxB.font = "bold 12.5px -apple-system, sans-serif";
      ctxB.fillText("Unfolded 2D Papercraft Cutout Net ∂G_λ(S) (λ=" + state.lambda.toFixed(2) + ") — Gem #" + gem.idx1 + " (hover face/edge)", 14, 20);

      // Compute bounding box of unfolded polygons + glue tabs
      let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
      Object.keys(net.polys).forEach(function (fKey) {
        net.polys[fKey].forEach(function (pt) {
          if (pt.x < minX) minX = pt.x;
          if (pt.x > maxX) maxX = pt.x;
          if (pt.y < minY) minY = pt.y;
          if (pt.y > maxY) maxY = pt.y;
        });
      });
      net.glueTabs.forEach(function (tab) {
        tab.poly.forEach(function (pt) {
          if (pt[0] < minX) minX = pt[0];
          if (pt[0] > maxX) maxX = pt[0];
          if (pt[1] < minY) minY = pt[1];
          if (pt[1] > maxY) maxY = pt[1];
        });
      });

      const padX = 28, padTop = 36, padBot = 44;
      const availW = WB - 2 * padX;
      const availH = HB - padTop - padBot;
      const spanX = Math.max(0.1, maxX - minX);
      const spanY = Math.max(0.1, maxY - minY);
      const sc = Math.min(availW / spanX, availH / spanY);
      const cx2 = 0.5 * (minX + maxX), cy2 = 0.5 * (minY + maxY);
      function mapX(x) { return WB * 0.5 + (x - cx2) * sc; }
      function mapY(y) { return padTop + availH * 0.5 - (y - cy2) * sc; }

      hitFaces2D = [];
      hitEdges2D = [];

      // 1. Draw Outward Trapezoidal Glue Tabs (N_tabs = f_0 - 1) + edge letters a, b, c...
      net.glueTabs.forEach(function (tab) {
        const isHovEdge = state.hoverEdge === tab.key;
        ctxB.fillStyle = isHovEdge ? "rgba(225, 29, 72, 0.35)" : "rgba(217, 130, 0, 0.26)";
        ctxB.strokeStyle = isHovEdge ? "#e11d48" : "#b86b00";
        ctxB.lineWidth = isHovEdge ? 2.0 : 1.05;
        ctxB.beginPath();
        tab.poly.forEach(function (pt, idx) {
          const xx = mapX(pt[0]), yy = mapY(pt[1]);
          if (idx === 0) ctxB.moveTo(xx, yy);
          else ctxB.lineTo(xx, yy);
        });
        ctxB.closePath();
        ctxB.fill();
        ctxB.stroke();
        if (tab.letter && tab.lblPos) {
          ctxB.save();
          ctxB.font = "bold 9px -apple-system, sans-serif";
          ctxB.fillStyle = isHovEdge ? "#e11d48" : "#92400e";
          ctxB.textAlign = "center";
          ctxB.textBaseline = "middle";
          ctxB.fillText(tab.letter, mapX(tab.lblPos[0]), mapY(tab.lblPos[1]));
          ctxB.restore();
        }
      });

      // 2. Draw Unfolded Polygonal Facets (f_2 faces)
      const fKeys = Object.keys(net.polys);
      fKeys.forEach(function (fKey, idx) {
        const poly = net.polys[fKey];
        const isHov = String(state.hoverFace) === String(fKey);
        const hue = 158 + (idx * 37) % 55;
        const light = 76 + (idx * 13) % 14;
        ctxB.fillStyle = isHov ? "rgba(250, 204, 21, 0.65)" : ("hsla(" + hue + ", 52%, " + light + "%, 0.86)");
        const screenPoly = [];
        ctxB.beginPath();
        poly.forEach(function (pt, k) {
          const xx = mapX(pt.x), yy = mapY(pt.y);
          screenPoly.push({ x: xx, y: yy });
          if (k === 0) ctxB.moveTo(xx, yy);
          else ctxB.lineTo(xx, yy);
        });
        ctxB.closePath();
        ctxB.fill();
        if (isHov) {
          ctxB.strokeStyle = "#d97706";
          ctxB.lineWidth = 2.4;
          ctxB.stroke();
        }
        hitFaces2D.push({ fi: String(fKey), poly: screenPoly });
      });

      // 3. Draw Interior Spanning-Tree Fold Lines (f_2 - 1 dashed lines)
      ctxB.save();
      net.foldEdges.forEach(function (fe) {
        const seg = fe.seg;
        const isHov = state.hoverEdge === fe.key;
        const a = { x: mapX(seg[0][0]), y: mapY(seg[0][1]) };
        const b = { x: mapX(seg[1][0]), y: mapY(seg[1][1]) };
        hitEdges2D.push({ key: fe.key, a: a, b: b });
        ctxB.strokeStyle = isHov ? "#e11d48" : "#0f6b52";
        ctxB.lineWidth = isHov ? 3.2 : 1.35;
        ctxB.setLineDash(isHov ? [] : [4, 3]);
        ctxB.beginPath();
        ctxB.moveTo(a.x, a.y);
        ctxB.lineTo(b.x, b.y);
        ctxB.stroke();
      });
      ctxB.restore();

      // 4. Draw Exterior Cut Boundary Edges (2 * (f_0 - 1) solid dark lines) + partner edge letters a, b, c...
      net.cutEdges.forEach(function (ce) {
        const seg = ce.seg;
        const isHov = state.hoverEdge === ce.key;
        const a = { x: mapX(seg[0][0]), y: mapY(seg[0][1]) };
        const b = { x: mapX(seg[1][0]), y: mapY(seg[1][1]) };
        hitEdges2D.push({ key: ce.key, a: a, b: b });
        ctxB.strokeStyle = isHov ? "#e11d48" : "#132a2c";
        ctxB.lineWidth = isHov ? 3.4 : 1.75;
        ctxB.beginPath();
        ctxB.moveTo(a.x, a.y);
        ctxB.lineTo(b.x, b.y);
        ctxB.stroke();
        if (!ce.hasTab && ce.letter && ce.partnerLblPos) {
          ctxB.save();
          ctxB.font = "bold 8.5px -apple-system, sans-serif";
          ctxB.fillStyle = isHov ? "#e11d48" : "#92400e";
          ctxB.textAlign = "center";
          ctxB.textBaseline = "middle";
          ctxB.fillText(ce.letter, mapX(ce.partnerLblPos[0]), mapY(ce.partnerLblPos[1]));
          ctxB.restore();
        }
      });

      // 5. Draw Vertex Number Labels s_ij in {1..16} inset toward each face centroid + ★ F0 at root facet
      ctxB.font = "bold 9.5px -apple-system, sans-serif";
      ctxB.textAlign = "center";
      ctxB.textBaseline = "middle";
      fKeys.forEach(function (fKey) {
        const poly = net.polys[fKey];
        let fcx = 0, fcy = 0;
        poly.forEach(function (pt) { fcx += pt.x; fcy += pt.y; });
        fcx /= poly.length; fcy /= poly.length;
        poly.forEach(function (pt) {
          const num = Math.round(gem.P_real[pt.vi][2] + 8.5);
          const lx = pt.x * 0.74 + fcx * 0.26;
          const ly = pt.y * 0.74 + fcy * 0.26;
          ctxB.fillStyle = "#132a2c";
          ctxB.fillText(String(num), mapX(lx), mapY(ly));
        });
        if (String(fKey) === String(net.rootIdx)) {
          ctxB.save();
          ctxB.font = "bold 10.5px -apple-system, sans-serif";
          ctxB.fillStyle = "#b45309";
          ctxB.fillText("★ F₀", mapX(fcx), mapY(fcy));
          ctxB.restore();
        }
      });
      ctxB.textAlign = "start";
      ctxB.textBaseline = "alphabetic";

      ctxB.font = "bold 11px -apple-system, sans-serif";
      ctxB.fillStyle = "#132a2c";
      ctxB.fillText(
        "f = (" + net.f0 + ", " + net.f1 + ", " + net.f2 + ") · " +
        (net.f2 - 1) + " Dashed Folds · " +
        net.cutEdges.length + " Cut Edges (a.." + String.fromCharCode(96 + Math.max(1, net.f0 - 1)) + ") · N_tabs = f₀ - 1 = " + (net.f0 - 1) + " Tabs",
        14, HB - 22
      );
      ctxB.fillStyle = "#b86b00";
      ctxB.fillText(
        "■ ★ F₀ = BFS Root Facet · Match letters a, b, c... on tabs & cut edges · Hover any face/edge to highlight in 3D!",
        14, HB - 7
      );
    }

    // ------------------- Printable Vector SVG Net Export -------------------
    function downloadPapercraftSVG() {
      const gem = getGem();
      const sk = skel();
      const net = sk.papercraft;
      const svgW = 900, svgH = 720;
      let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
      Object.keys(net.polys).forEach(function (fKey) {
        net.polys[fKey].forEach(function (pt) {
          if (pt.x < minX) minX = pt.x;
          if (pt.x > maxX) maxX = pt.x;
          if (pt.y < minY) minY = pt.y;
          if (pt.y > maxY) maxY = pt.y;
        });
      });
      net.glueTabs.forEach(function (tab) {
        tab.poly.forEach(function (pt) {
          if (pt[0] < minX) minX = pt[0];
          if (pt[0] > maxX) maxX = pt[0];
          if (pt[1] < minY) minY = pt[1];
          if (pt[1] > maxY) maxY = pt[1];
        });
      });
      const padX = 56, padTop = 86, padBot = 86;
      const availW = svgW - 2 * padX - 150, availH = svgH - padTop - padBot;
      const sc = Math.min(availW / Math.max(0.1, maxX - minX), availH / Math.max(0.1, maxY - minY));
      const cx2 = 0.5 * (minX + maxX), cy2 = 0.5 * (minY + maxY);
      const netCenterX = padX + availW * 0.5;
      function sx(x) { return (netCenterX + (x - cx2) * sc).toFixed(2); }
      function sy(y) { return (padTop + availH * 0.5 - (y - cy2) * sc).toFixed(2); }

      const lines = [];
      lines.push('<?xml version="1.0" encoding="UTF-8"?>');
      lines.push('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + svgW + ' ' + svgH + '" width="' + svgW + '" height="' + svgH + '" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif">');
      lines.push('  <rect width="100%" height="100%" fill="#ffffff"/>');
      lines.push('  <text x="36" y="38" font-size="18" font-weight="bold" fill="#132a2c">Buildable 2D Papercraft Cutout Net ∂G_λ(S) — Frénicle #' + gem.idx1 + ' (λ = ' + state.lambda.toFixed(2) + ')</text>');
      lines.push('  <text x="36" y="58" font-size="12.5" fill="#475569">f = (' + net.f0 + ', ' + net.f1 + ', ' + net.f2 + ') · ' + (net.f2 - 1) + ' Dashed Mountain Fold Lines · ' + net.cutEdges.length + ' Solid Cut Edges · N_tabs = f₀ − 1 = ' + (net.f0 - 1) + ' Trapezoidal Glue Tabs (match letters a, b, c...)</text>');

      // 0. 4x4 Magic-Square Legend Box (top-right corner)
      const innerMap = {};
      (gem.inner_idx || []).forEach(function (vi) { innerMap[vi] = true; });
      const legX = svgW - 148, legY = 18, cellSz = 26, cellGap = 2;
      const legW = 4 * cellSz + 3 * cellGap + 16, legH = 4 * cellSz + 3 * cellGap + 42;
      lines.push('  <g id="magic-square-legend">');
      lines.push('    <rect x="' + legX + '" y="' + legY + '" width="' + legW + '" height="' + legH + '" rx="7" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2"/>');
      lines.push('    <text x="' + (legX + legW * 0.5) + '" y="' + (legY + 15) + '" font-size="10.5" font-weight="bold" fill="#132a2c" text-anchor="middle">4×4 Square #' + gem.idx1 + ' (V₀=' + (16 - (gem.inner_idx || []).length) + ', V₁=' + (gem.inner_idx || []).length + ')</text>');
      for (let r = 0; r < 4; r++) {
        for (let c = 0; c < 4; c++) {
          const k = r * 4 + c;
          const isIn = !!innerMap[k];
          const cx = legX + 8 + c * (cellSz + cellGap);
          const cy = legY + 22 + r * (cellSz + cellGap);
          const bg = isIn ? "#fef3c7" : "#e0f2fe";
          const bdr = isIn ? "#d97706" : "#0284c7";
          lines.push('    <rect x="' + cx + '" y="' + cy + '" width="' + cellSz + '" height="' + cellSz + '" fill="' + bg + '" stroke="' + bdr + '" stroke-width="1.1"/>');
          lines.push('    <text x="' + (cx + cellSz * 0.5) + '" y="' + (cy + cellSz * 0.52) + '" font-size="11" font-weight="bold" fill="#132a2c" text-anchor="middle" dominant-baseline="central">' + gem.S[r][c] + '</text>');
        }
      }
      lines.push('    <text x="' + (legX + legW * 0.5) + '" y="' + (legY + legH - 6) + '" font-size="9" fill="#475569" text-anchor="middle">Blue = Hull V₀ · Amber = Core V₁</text>');
      lines.push('  </g>');

      // 1. Grey trapezoidal glue tabs
      net.glueTabs.forEach(function (tab) {
        const ptsStr = tab.poly.map(function (pt) { return sx(pt[0]) + "," + sy(pt[1]); }).join(" ");
        lines.push('  <polygon points="' + ptsStr + '" fill="#e2e8f0" stroke="#475569" stroke-width="1.2"/>');
        if (tab.letter && tab.lblPos) {
          lines.push('  <text x="' + sx(tab.lblPos[0]) + '" y="' + sy(tab.lblPos[1]) + '" font-size="11" font-weight="bold" fill="#1e293b" text-anchor="middle" dominant-baseline="central">' + tab.letter + '</text>');
        }
      });

      // 2. Unfolded polygonal facets
      const fKeys = Object.keys(net.polys);
      fKeys.forEach(function (fKey, idx) {
        const poly = net.polys[fKey];
        const hue = 158 + (idx * 37) % 55;
        const light = 82 + (idx * 11) % 10;
        const ptsStr = poly.map(function (pt) { return sx(pt.x) + "," + sy(pt.y); }).join(" ");
        lines.push('  <polygon points="' + ptsStr + '" fill="hsl(' + hue + ', 48%, ' + light + '%)" fill-opacity="0.78" stroke="none"/>');
      });

      // 3. Dashed interior fold lines
      net.foldEdges.forEach(function (fe) {
        const seg = fe.seg;
        lines.push('  <line x1="' + sx(seg[0][0]) + '" y1="' + sy(seg[0][1]) + '" x2="' + sx(seg[1][0]) + '" y2="' + sy(seg[1][1]) + '" stroke="#0f6b52" stroke-width="1.6" stroke-dasharray="6,4"/>');
      });

      // 4. Solid exterior cut edges + partner letter labels
      net.cutEdges.forEach(function (ce) {
        const seg = ce.seg;
        lines.push('  <line x1="' + sx(seg[0][0]) + '" y1="' + sy(seg[0][1]) + '" x2="' + sx(seg[1][0]) + '" y2="' + sy(seg[1][1]) + '" stroke="#132a2c" stroke-width="2.1"/>');
        if (!ce.hasTab && ce.letter && ce.partnerLblPos) {
          lines.push('  <text x="' + sx(ce.partnerLblPos[0]) + '" y="' + sy(ce.partnerLblPos[1]) + '" font-size="10.5" font-weight="bold" fill="#334155" text-anchor="middle" dominant-baseline="central">' + ce.letter + '</text>');
        }
      });

      // 5. Vertex labels 1..16 and ★ F0 root marker
      fKeys.forEach(function (fKey) {
        const poly = net.polys[fKey];
        let fcx = 0, fcy = 0;
        poly.forEach(function (pt) { fcx += pt.x; fcy += pt.y; });
        fcx /= poly.length; fcy /= poly.length;
        poly.forEach(function (pt) {
          const num = Math.round(gem.P_real[pt.vi][2] + 8.5);
          const lx = pt.x * 0.74 + fcx * 0.26;
          const ly = pt.y * 0.74 + fcy * 0.26;
          lines.push('  <text x="' + sx(lx) + '" y="' + sy(ly) + '" font-size="11.5" font-weight="bold" fill="#132a2c" text-anchor="middle" dominant-baseline="central">' + num + '</text>');
        });
        if (String(fKey) === String(net.rootIdx)) {
          lines.push('  <text x="' + sx(fcx) + '" y="' + sy(fcy) + '" font-size="13" font-weight="bold" fill="#b45309" text-anchor="middle" dominant-baseline="central">★ F₀</text>');
        }
      });

      lines.push('  <text x="36" y="' + (svgH - 24) + '" font-size="12" fill="#0f6b52" font-weight="bold">Instructions: Cut along solid dark outer borders (including grey glue tabs), score &amp; fold along dashed green lines, and glue each tab (a, b, c...) under its matching lettered edge.</text>');
      lines.push('</svg>');

      const blob = new Blob([lines.join("\n")], { type: "image/svg+xml;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "magicGem_" + gem.idx1 + "_lam" + state.lambda.toFixed(2) + "_net.svg";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
    }

    function distToSeg2D(px, py, a, b) {
      const dx = b.x - a.x, dy = b.y - a.y;
      const l2 = dx * dx + dy * dy;
      if (l2 < 1e-9) return Math.hypot(px - a.x, py - a.y);
      const t = Math.max(0, Math.min(1, ((px - a.x) * dx + (py - a.y) * dy) / l2));
      return Math.hypot(px - (a.x + t * dx), py - (a.y + t * dy));
    }

    function ptInScreenPoly(px, py, poly) {
      let inside = false;
      for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
        const xi = poly[i].x, yi = poly[i].y;
        const xj = poly[j].x, yj = poly[j].y;
        const intersect = ((yi > py) !== (yj > py)) && (px < (xj - xi) * (py - yi) / ((yj - yi) || 1e-12) + xi);
        if (intersect) inside = !inside;
      }
      return inside;
    }

    canvasBal.addEventListener("mousemove", function (ev) {
      if (state.right !== "paper") return;
      const rect = canvasBal.getBoundingClientRect();
      const mx = (ev.clientX - rect.left) * (canvasBal.width / rect.width);
      const my = (ev.clientY - rect.top) * (canvasBal.height / rect.height);
      let newEdge = null;
      let bestDist = 7.5;
      hitEdges2D.forEach(function (he) {
        const d = distToSeg2D(mx, my, he.a, he.b);
        if (d < bestDist) { bestDist = d; newEdge = he.key; }
      });
      let newFace = null;
      if (!newEdge) {
        for (let i = 0; i < hitFaces2D.length; i++) {
          if (ptInScreenPoly(mx, my, hitFaces2D[i].poly)) {
            newFace = hitFaces2D[i].fi;
            break;
          }
        }
      }
      if (newEdge !== state.hoverEdge || newFace !== state.hoverFace) {
        state.hoverEdge = newEdge;
        state.hoverFace = newFace;
        dirty = true;
      }
    });
    canvasBal.addEventListener("mouseleave", function () {
      if (state.hoverEdge !== null || state.hoverFace !== null) {
        state.hoverEdge = null;
        state.hoverFace = null;
        dirty = true;
      }
    });

    canvas3d.addEventListener("mousemove", function (ev) {
      if (ev.buttons !== 0) return;
      const rect = canvas3d.getBoundingClientRect();
      const mx = (ev.clientX - rect.left) * (canvas3d.width / rect.width);
      const my = (ev.clientY - rect.top) * (canvas3d.height / rect.height);
      let newEdge = null;
      let bestDist = 7.5;
      hitEdges3D.forEach(function (he) {
        const d = distToSeg2D(mx, my, he.a, he.b);
        if (d < bestDist) { bestDist = d; newEdge = he.key; }
      });
      let newFace = null;
      if (!newEdge && hitFaces3D.length > 0) {
        const sorted = hitFaces3D.slice().sort(function (a, b) { return b.depth - a.depth; });
        for (let i = 0; i < sorted.length; i++) {
          if (ptInScreenPoly(mx, my, sorted[i].poly)) {
            newFace = sorted[i].fi;
            break;
          }
        }
      }
      if (newEdge !== state.hoverEdge || newFace !== state.hoverFace) {
        state.hoverEdge = newEdge;
        state.hoverFace = newFace;
        dirty = true;
      }
    });
    canvas3d.addEventListener("mouseleave", function () {
      if (state.hoverEdge !== null || state.hoverFace !== null) {
        state.hoverEdge = null;
        state.hoverFace = null;
        dirty = true;
      }
    });

    function updateReadout(gem, st) {
      const fmt = function (v) { return (Math.abs(v) < 1e-9 ? 0 : v).toFixed(4); };
      const ok = vecNorm(st.comp) < 5e-4;
      const sk = skel();
      let first;
      if (state.right === "paper") {
        first = "<span>Papercraft net (λ=" + state.lambda.toFixed(2) + "): <span class='hl'>" + sk.papercraft.f2 + " faces, " + (sk.papercraft.f2 - 1) + " folds, " + (sk.papercraft.f0 - 1) + " glue tabs</span> (N_tabs = f₀ − 1)</span>";
      } else if (state.fab === "wireframe") {
        first = "<span>Rod length (λ=" + state.lambda.toFixed(2) + "): outer <span class='hl'>" + sk.st0.L.toFixed(2) + "</span>, inner <span class='hl'>" + sk.st1.L.toFixed(2) + "</span></span>";
      } else {
        first = "<span>K₁₆ (λ=" + state.lambda.toFixed(2) + "): <span class='hl'>120 rods</span>, total length <span class='hl'>" + sk.stK16.L.toFixed(1) + "</span></span>";
      }
      readout.innerHTML = first +
        "<span>Centre of mass = <span class='" + (ok ? "hl" : "warn") + "'>(" + fmt(st.comp[0]) + ", " + fmt(st.comp[1]) + ", " + fmt(st.comp[2]) + ")</span></span>" +
        "<span>Seesaw: <span class='" + (ok ? "hl" : "warn") + "'>" + (ok ? "LEVEL ✓" : (state.tiltCur * 180 / Math.PI).toFixed(1) + "° tilt") + "</span></span>";
    }

    function snap() {
      const tgt = balanceTarget();
      if (!tgt) return;
      state.rhoAnim = { from: state.param, to: tgt.val, t0: performance.now(), dur: 1000, label: tgt.label };
    }
    function setFab(f) {
      state.fab = f;
      state.rhoAnim = null;
      setParam(f === "k16" ? 1 : 0);
      updateControls();
    }

    sqSelect.addEventListener("change", function () {
      state.sqKey = sqSelect.value;
      state.rhoAnim = null;
      state.hoverFace = null;
      state.hoverEdge = null;
      setParam(state.fab === "k16" ? 1 : 0);
      updateControls();
    });
    if (lamSelect) {
      lamSelect.addEventListener("change", function () {
        state.lambda = parseFloat(lamSelect.value) || 1.00;
        state.rhoAnim = null;
        state.hoverFace = null;
        state.hoverEdge = null;
        if (state.fab === "wireframe" && state.param > 0) {
          const tgt = balanceTarget();
          if (tgt) setParam(tgt.val, tgt.label);
          else setParam(0);
        } else {
          setParam(state.fab === "k16" ? state.param : 0);
        }
        updateControls();
        dirty = true;
      });
    }
    fabTabs.forEach(function (b) { b.addEventListener("click", function () { setFab(b.getAttribute("data-fab")); }); });
    rightBtns.forEach(function (b) {
      b.addEventListener("click", function () { state.right = b.getAttribute("data-fab-right"); updateControls(); dirty = true; });
    });
    rhoSlider.addEventListener("input", function () { state.rhoAnim = null; setParam(parseFloat(rhoSlider.value)); });
    peelSlider.addEventListener("input", function () { state.peelAnim = null; setPeel(parseFloat(peelSlider.value)); });
    btnSnap.addEventListener("click", snap);
    btnReset.addEventListener("click", function () {
      state.rhoAnim = { from: state.param, to: state.fab === "k16" ? 1 : 0, t0: performance.now(), dur: 700, label: null };
    });
    if (btnPeelAnim) {
      btnPeelAnim.addEventListener("click", function () {
        state.peelAnim = { from: state.peel, t0: performance.now(), dur: 2600 };
      });
    }
    if (btnSvg) {
      btnSvg.addEventListener("click", function () {
        state.right = "paper";
        updateControls();
        dirty = true;
        downloadPapercraftSVG();
      });
    }
    if (btnLens) {
      btnLens.addEventListener("click", function () {
        state.showLens = !state.showLens;
        btnLens.classList.toggle("active", state.showLens);
        dirty = true;
      });
    }

    window.MG_SIM_FAB = {
      load: function (o) {
        o = o || {};
        if (o.sq) { state.sqKey = String(o.sq); sqSelect.value = state.sqKey; }
        if (o.lam !== undefined) { state.lambda = parseFloat(o.lam); if (lamSelect) lamSelect.value = state.lambda.toFixed(2); }
        if (o.fab) state.fab = o.fab;
        if (o.right) state.right = o.right;
        state.rhoAnim = null;
        state.hoverFace = null;
        state.hoverEdge = null;
        setParam(state.fab === "k16" ? 1 : 0);
        state.tiltCur = 0;
        updateControls();
        if (o.snap) setTimeout(snap, 650);
        if (o.peel) state.peelAnim = { from: state.peel, t0: performance.now(), dur: 2600 };
        dirty = true;
      },
      preset: function (name) {
        const P = {
          wire673: { sq: "673", lam: 1.00, fab: "wireframe", right: "seesaw", snap: true },
          k16net: { sq: "673", lam: 1.00, fab: "k16", right: "seesaw", snap: true },
          paper175: { sq: "175", lam: 0.20, fab: "k16", right: "paper" }
        };
        if (P[name]) this.load(P[name]);
      }
    };

    function frame(now) {
      if (state.rhoAnim) {
        const a = state.rhoAnim;
        const t = Math.min(1, (now - a.t0) / a.dur);
        setParam(a.from + (a.to - a.from) * easeInOut(t), t >= 1 ? a.label : null);
        if (t >= 1) state.rhoAnim = null;
      }
      if (state.peelAnim) {
        const a = state.peelAnim;
        const t = Math.min(1, (now - a.t0) / a.dur);
        setPeel(t < 0.5 ? a.from + (0.9 - a.from) * easeInOut(t * 2) : 0.9 + (0.15 - 0.9) * easeInOut(t * 2 - 1));
        if (t >= 1) state.peelAnim = null;
      }
      const gem = getGem();
      const st = stats(state.param);
      const ax = axisOf(st);
      const tgt = targetTilt(st.comp[ax]);
      if (Math.abs(tgt - state.tiltCur) > 1e-4) {
        state.tiltCur += (tgt - state.tiltCur) * 0.1;
        if (state.right === "seesaw") dirty = true;
      }
      if (dirty && isVisible("sim-fab")) {
        render3D(gem, st, ax);
        if (state.right === "paper") renderPapercraft(gem, skel());
        else renderSeesaw(gem, st, ax);
        updateReadout(gem, st);
        dirty = false;
      }
      requestAnimationFrame(frame);
    }
    updateControls();
    requestAnimationFrame(frame);
  }

  // =========================================================================
  // SIMULATOR 5: Mirror-Twin Tower Builder & Tilting-Table Toppling Simulator
  // =========================================================================
  function initSim4() {
    const sqSelect = document.getElementById("stack-sq-select");
    const modeSelect = document.getElementById("stack-mode-select");
    const lamSlider = document.getElementById("stack-lam-slider");
    const lamVal = document.getElementById("stack-lam-val");
    const tiltSlider = document.getElementById("stack-tilt-slider");
    const tiltVal = document.getElementById("stack-tilt-val");
    const btnZero = document.getElementById("btn-tilt-zero");
    const btnCrit = document.getElementById("btn-tilt-crit");
    const btnTopple = document.getElementById("btn-tilt-topple");
    const btnLens = document.getElementById("btn-stack-lens");
    const canvas3d = document.getElementById("canvas-stack-3d");
    const canvasFoot = document.getElementById("canvas-stack-footprint");
    const readout = document.getElementById("stack-readout");
    if (!canvas3d || !canvasFoot) return;

    const ctx3 = canvas3d.getContext("2d");
    const ctxF = canvasFoot.getContext("2d");

    const cam = { yaw: -0.52, pitch: 0.26 };
    attachOrbitControl(canvas3d, cam, renderSim4);

    // Footprint metadata for the 4 featured stacking gems
    const TOWER_META = {
      "763": {
        name: "#763 (0-idx #762)",
        area: 5.0,
        zCtr: 6.0,
        sameParallel: false,
        planeTop: [4, -3, 5, -60],
        planeBot: [-4, -3, -5, -60],
        poly: [[-1.5, 0.5], [-0.5, -1.5], [1.5, -0.5], [0.5, 1.5]],
        topVerts: [4, 13, 11, 2],
        botVerts: [8, 1, 7, 14]
      },
      "603": {
        name: "#603 (0-idx #602)",
        area: 5.0,
        zCtr: 5.0,
        sameParallel: false,
        planeTop: [2, -9, 5, -50],
        planeBot: [-2, -9, -5, -50],
        poly: [[-1.5, 0.5], [-0.5, -1.5], [1.5, -0.5], [0.5, 1.5]],
        topVerts: [4, 13, 11, 2],
        botVerts: [8, 1, 7, 14]
      },
      "774": {
        name: "#774 (0-idx #773)",
        area: 5.0,
        zCtr: 6.0,
        sameParallel: true,
        planeTop: [1, 0, 1, -12],
        planeBot: [-1, 0, -1, -12],
        poly: [[-1.5, 0.5], [-0.5, -1.5], [1.5, -0.5], [0.5, 1.5]],
        topVerts: [4, 13, 11, 2],
        botVerts: [8, 1, 7, 14]
      },
      "756": {
        name: "#756 (0-idx #755)",
        area: 4.0,
        zCtr: 6.0,
        sameParallel: false,
        planeTop: [5, -3, 4, -48],
        planeBot: [-5, -3, -4, -48],
        poly: [[-1.5, 0.5], [0.5, -1.5], [1.5, -0.5], [-0.5, 1.5]],
        topVerts: [8, 2, 13, 7],
        botVerts: [1, 11, 4, 14]
      }
    };

    let state = {
      sqKey: "763",
      mode: "twin", // "twin" | "same"
      lambda: 0.20,
      tiltDeg: 0.0,
      topplePhase: 0.0,
      dropPhase: 4.0,   // < 4 while blocks are still falling into place
      tiltAnim: null,
      showLens: true
    };

    // Exact 3D facet stability margin d_stab(lambda) and critical tipping angle theta_tip(lambda)
    // matching verify_paper_c.py :: facet_stability_at_lambda
    function computeExactFacetStability(gem, meta, lam) {
      const a = meta.planeBot[0], b = meta.planeBot[1], c = meta.planeBot[2];
      const nVec = [a * lam, b * lam, c];
      const nHat = vecNormalize(nVec);
      const ptsF = meta.botVerts.map(function (vi) {
        const p = gem.P_real[vi];
        return [p[0], p[1], p[2] * lam];
      });
      const comLam = [gem.c0[0], gem.c0[1], gem.c0[2] * lam];
      let ref = Math.abs(nHat[0]) < 0.9 ? [1, 0, 0] : [0, 1, 0];
      const dotRef = vecDot(ref, nHat);
      const e1 = vecNormalize(vecSub(ref, vecScale(nHat, dotRef)));
      const e2 = vecCross(nHat, e1);
      const orig = ptsF[0];
      const uv = ptsF.map(function (p) {
        const d = vecSub(p, orig);
        return [vecDot(d, e1), vecDot(d, e2)];
      });
      let cx = 0, cy = 0;
      uv.forEach(function (u) { cx += u[0]; cy += u[1]; });
      cx /= uv.length; cy /= uv.length;
      uv.sort(function (u, v) {
        return Math.atan2(u[1] - cy, u[0] - cx) - Math.atan2(v[1] - cy, v[0] - cx);
      });
      const hCom = -vecDot(vecSub(comLam, orig), nHat);
      const comD = vecSub(comLam, orig);
      const comUV = [vecDot(comD, e1), vecDot(comD, e2)];
      let minDist = Infinity;
      let steepVec = [2 / Math.sqrt(5), -1 / Math.sqrt(5)];
      const m = uv.length;
      for (let i = 0; i < m; i++) {
        const u0 = uv[i];
        const u1 = uv[(i + 1) % m];
        const dx = u1[0] - u0[0];
        const dy = u1[1] - u0[1];
        const len = Math.hypot(dx, dy);
        const dist = (dx * (comUV[1] - u0[1]) - dy * (comUV[0] - u0[0])) / len;
        if (dist < minDist) {
          minDist = dist;
          const n3 = vecAdd(vecScale(e1, dy / len), vecScale(e2, -dx / len));
          const nh = Math.hypot(n3[0], n3[1]);
          if (nh > 1e-9) steepVec = [n3[0] / nh, n3[1] / nh];
        }
      }
      const critDeg = minDist > 0 ? (Math.atan2(minDist, hCom) * 180) / Math.PI : 0.0;
      const jointTan = Math.hypot(a, b) * lam / Math.abs(c);
      const jointDeg = (Math.atan(jointTan) * 180) / Math.PI;
      return {
        dStab: minDist,
        hCom: hCom,
        critDeg: critDeg,
        dirX: steepVec[0],
        dirY: steepVec[1],
        jointTan: jointTan,
        jointDeg: jointDeg
      };
    }

    function getTowerStatus() {
      const gem = GEMS[state.sqKey] || GEMS["763"];
      const meta = TOWER_META[state.sqKey] || TOWER_META["763"];
      const exact = computeExactFacetStability(gem, meta, state.lambda);
      const mismatched = state.mode === "same" && !meta.sameParallel;
      const toppled = mismatched || state.tiltDeg > exact.critDeg;
      return {
        meta: meta,
        dStab: exact.dStab,
        hHalf: exact.hCom,
        critDeg: exact.critDeg,
        dirX: exact.dirX,
        dirY: exact.dirY,
        jointTan: exact.jointTan,
        jointDeg: exact.jointDeg,
        mismatched: mismatched,
        toppled: toppled
      };
    }

    // Rotate 3D point by exact angle `ang` around the horizontal axis [-dirY, dirX, 0]
    // so the tower tilts toward (dirX, dirY) by the exact table angle `ang`
    function rotateAlongTiltDir(pt, ang, dirX, dirY) {
      const R = rodriguesExp([-dirY, dirX, 0], ang);
      return matVec(R, pt);
    }

    function renderSim4() {
      const gem = GEMS[state.sqKey] || GEMS["763"];
      const st = getTowerStatus();
      const meta = st.meta;

      // ----- Left Canvas: True 3D Polyhedral 4-Block Tower on Tilting Table -----
      const W = canvas3d.width;
      const H = canvas3d.height;
      ctx3.clearRect(0, 0, W, H);

      ctx3.fillStyle = "#132a2c";
      ctx3.font = "bold 12.5px -apple-system, sans-serif";
      ctx3.fillText(
        "3D Polyhedral Tower — " + meta.name + " (" + (state.mode === "twin" ? "Mirror Twins Locked" : "Same Gem Only") + ")",
        14,
        20
      );

      const scale3d = 28;
      const visLam = Math.max(0.14, Math.min(0.28, state.lambda));
      const blockDz = 2 * meta.zCtr * visLam;
      const towerBaseZ = -2.0 * blockDz;
      const tiltRad = (state.tiltDeg * Math.PI) / 180;
      const dirX = st.dirX, dirY = st.dirY;

      // Draw Tilted 3D Plinth / Table at exact tiltRad along (dirX, dirY)
      const plinthCorners = [
        [-2.4, -2.4, towerBaseZ],
        [2.4, -2.4, towerBaseZ],
        [2.4, 2.4, towerBaseZ],
        [-2.4, 2.4, towerBaseZ]
      ].map(function (p) {
        const tilted = rotateAlongTiltDir([p[0], p[1], p[2] - towerBaseZ], tiltRad, dirX, dirY);
        return project3D([tilted[0], tilted[1], tilted[2] + towerBaseZ * 0.85], cam, W, H, scale3d);
      });
      ctx3.fillStyle = "rgba(44, 58, 55, 0.25)";
      ctx3.strokeStyle = "#2c3a37";
      ctx3.lineWidth = 2.0;
      ctx3.beginPath();
      plinthCorners.forEach(function (pt, i) {
        if (i === 0) ctx3.moveTo(pt.x, pt.y);
        else ctx3.lineTo(pt.x, pt.y);
      });
      ctx3.closePath();
      ctx3.fill();
      ctx3.stroke();

      // Build and render all 4 3D polyhedral blocks B_0, B_1, B_2, B_3
      const allFaces3D = [];
      for (let k = 0; k < 4; k++) {
        if (state.dropPhase <= k) continue;
        const isTwin = state.mode === "twin" && (k % 2 === 1);
        const fall = Math.min(1, state.dropPhase - k);
        const dropOff = (1 - easeOutBounce(fall)) * 7.0;
        const zCenter = towerBaseZ + (k + 0.5) * blockDz + dropOff;
        const toppleAng = (st.toppled && k >= 1)
          ? state.topplePhase * (0.16 + 0.12 * k) * (st.mismatched ? -1 : 1)
          : 0;
        const mismatchShiftX = (st.mismatched && k >= 1) ? (k % 2 === 1 ? -0.45 : 0.35) : 0;

        const blockVerts = gem.P_real.map(function (p) {
          const sgn = isTwin ? -1 : 1;
          let bx = sgn * p[0] + mismatchShiftX;
          let by = sgn * p[1];
          let bz = sgn * p[2] * visLam;
          if (toppleAng !== 0) {
            const relZ = bz + 0.5 * blockDz;
            const rot = rotateAlongTiltDir([bx - 0.8 * dirX, by - 0.8 * dirY, relZ], toppleAng, dirX, dirY);
            bx = rot[0] + 0.8 * dirX;
            by = rot[1] + 0.8 * dirY;
            bz = rot[2] - 0.5 * blockDz;
          }
          const worldPt = [bx, by, zCenter + bz];
          const tilted = rotateAlongTiltDir([worldPt[0], worldPt[1], worldPt[2] - towerBaseZ], tiltRad, dirX, dirY);
          return [tilted[0], tilted[1], tilted[2] + towerBaseZ * 0.85];
        });

        gem.faces0.forEach(function (f) {
          const fPts = f.verts.map(function (vi) { return blockVerts[vi]; });
          let cx = 0, cy = 0, cz = 0;
          fPts.forEach(function (p) { cx += p[0]; cy += p[1]; cz += p[2]; });
          cx /= fPts.length; cy /= fPts.length; cz /= fPts.length;
          const pr = project3D([cx, cy, cz], cam, W, H, scale3d);
          const isContact = (f.verts.length === 4) && (
            f.verts.every(function (v) { return meta.topVerts.indexOf(v) !== -1; }) ||
            f.verts.every(function (v) { return meta.botVerts.indexOf(v) !== -1; })
          );
          allFaces3D.push({
            pts: fPts,
            depth: pr.depth,
            isTwin: isTwin,
            isContact: isContact
          });
        });
      }

      allFaces3D.sort(function (a, b) { return a.depth - b.depth; });
      allFaces3D.forEach(function (f) {
        const p2d = f.pts.map(function (p) { return project3D(p, cam, W, H, scale3d); });
        if (f.isContact) {
          ctx3.fillStyle = st.mismatched ? "rgba(217, 27, 66, 0.88)" : "rgba(59, 232, 176, 0.88)";
          ctx3.strokeStyle = "#102526";
          ctx3.lineWidth = 1.6;
        } else if (f.isTwin) {
          ctx3.fillStyle = "rgba(217, 130, 0, 0.76)";
          ctx3.strokeStyle = "rgba(95, 55, 0, 0.72)";
          ctx3.lineWidth = 0.95;
        } else {
          ctx3.fillStyle = "rgba(15, 107, 82, 0.76)";
          ctx3.strokeStyle = "rgba(10, 45, 36, 0.72)";
          ctx3.lineWidth = 0.95;
        }
        ctx3.beginPath();
        p2d.forEach(function (pt, idx) {
          if (idx === 0) ctx3.moveTo(pt.x, pt.y);
          else ctx3.lineTo(pt.x, pt.y);
        });
        ctx3.closePath();
        ctx3.fill();
        ctx3.stroke();
      });

      // When Same Gem Only is selected and slopes mismatch, draw +n_+ and -n_- vectors at the first joint
      if (st.mismatched) {
        const jZ = towerBaseZ + blockDz;
        const jOrigin3 = rotateAlongTiltDir([0, 0, jZ - towerBaseZ], tiltRad, dirX, dirY);
        const pJoint = project3D([jOrigin3[0], jOrigin3[1], jOrigin3[2] + towerBaseZ * 0.85], cam, W, H, scale3d);
        const nTopRaw = vecNormalize([meta.planeTop[0] * visLam, meta.planeTop[1] * visLam, meta.planeTop[2]]);
        const negNBotRaw = vecNormalize([-meta.planeBot[0] * visLam, -meta.planeBot[1] * visLam, -meta.planeBot[2]]);
        const nTop3 = rotateAlongTiltDir([nTopRaw[0] * 1.65, nTopRaw[1] * 1.65, jZ + nTopRaw[2] * 1.65 - towerBaseZ], tiltRad, dirX, dirY);
        const negBot3 = rotateAlongTiltDir([negNBotRaw[0] * 1.65, negNBotRaw[1] * 1.65, jZ + negNBotRaw[2] * 1.65 - towerBaseZ], tiltRad, dirX, dirY);
        const pTopTip = project3D([nTop3[0], nTop3[1], nTop3[2] + towerBaseZ * 0.85], cam, W, H, scale3d);
        const pBotTip = project3D([negBot3[0], negBot3[1], negBot3[2] + towerBaseZ * 0.85], cam, W, H, scale3d);
        drawArrow2D(ctx3, pJoint.x, pJoint.y, pTopTip.x, pTopTip.y, "#059669", 3.0, 9);
        drawArrow2D(ctx3, pJoint.x, pJoint.y, pBotTip.x, pBotTip.y, "#e11d48", 3.0, 9);
        ctx3.save();
        ctx3.font = "bold 11.5px -apple-system, sans-serif";
        ctx3.fillStyle = "#047857";
        ctx3.fillText("+n₊", pTopTip.x + 6, pTopTip.y - 3);
        ctx3.fillStyle = "#be123c";
        ctx3.fillText("−n₋", pBotTip.x - 28, pBotTip.y - 3);
        const wedgeDeg = (2 * Math.atan(Math.abs(meta.planeTop[0]) * state.lambda / Math.abs(meta.planeTop[2])) * 180 / Math.PI).toFixed(1);
        ctx3.fillStyle = "rgba(255, 241, 242, 0.94)";
        ctx3.strokeStyle = "#e11d48";
        ctx3.lineWidth = 1.4;
        ctx3.fillRect(14, 30, 268, 22);
        ctx3.strokeRect(14, 30, 268, 22);
        ctx3.fillStyle = "#9f1239";
        ctx3.font = "bold 11px -apple-system, sans-serif";
        ctx3.fillText("Wedge gap 2θ_x = " + wedgeDeg + "°: n₋ ≠ −n₊ (slopes clash!)", 20, 45);
        ctx3.restore();
      }

      if (state.showLens) {
        drawSquareLensHUD(ctx3, gem.S, {
          x: W - 118,
          y: 28,
          size: 104,
          mode: "stacking",
          topVerts: meta.topVerts,
          botVerts: meta.botVerts,
          title: "#" + gem.idx1 + " · F₊/F₋"
        });
      }

      // Legend at bottom of Left Canvas
      ctx3.font = "bold 11.5px -apple-system, sans-serif";
      ctx3.fillStyle = "#0f6b52";
      ctx3.fillText("■ Primary Gem G_λ(S)", 14, H - 10);
      ctx3.fillStyle = "#b86b00";
      ctx3.fillText("■ Mirror Twin G_λ(r²S̄) = -G_λ(S)", 160, H - 10);
      ctx3.fillStyle = st.toppled ? "#d91b42" : "#0f6b52";
      ctx3.fillText(st.toppled ? "⚠ TOPPLING / MISMATCHED" : "✓ 100% 3D Facet Lock", 362, H - 10);

      // ----- Right Canvas: Top-Down Support Footprint & Projected CoM Trajectory -----
      const WF = canvasFoot.width;
      const HF = canvasFoot.height;
      ctxF.clearRect(0, 0, WF, HF);

      ctxF.fillStyle = "#132a2c";
      ctxF.font = "bold 12.5px -apple-system, sans-serif";
      ctxF.fillText(
        "Top-Down Support Polygon F_- (Area A_xy = " + meta.area.toFixed(1) + ") & CoM Tipping Margin",
        14,
        20
      );

      const cx = WF * 0.5;
      const cy = HF * 0.53;
      const scale = 86;

      // Draw 4x4 grid dots
      GRID_XY.forEach(function (cell) {
        const px = cx + cell.x * scale;
        const py = cy - cell.y * scale;
        ctxF.strokeStyle = "#e2e8e5";
        ctxF.strokeRect(px - scale * 0.5, py - scale * 0.5, scale, scale);
        ctxF.fillStyle = "#95a59f";
        ctxF.beginPath();
        ctxF.arc(px, py, 3, 0, Math.PI * 2);
        ctxF.fill();
      });

      // Draw support polygon F_-
      ctxF.fillStyle = st.toppled ? "rgba(217, 27, 66, 0.16)" : "rgba(15, 107, 82, 0.20)";
      ctxF.strokeStyle = st.toppled ? "#d91b42" : "#0f6b52";
      ctxF.lineWidth = 2.8;
      ctxF.beginPath();
      meta.poly.forEach(function (pt, idx) {
        const px = cx + pt[0] * scale;
        const py = cy - pt[1] * scale;
        if (idx === 0) ctxF.moveTo(px, py);
        else ctxF.lineTo(px, py);
      });
      ctxF.closePath();
      ctxF.fill();
      ctxF.stroke();

      // Draw stability circle of radius d_stab
      ctxF.save();
      ctxF.strokeStyle = "#d98200";
      ctxF.lineWidth = 1.6;
      ctxF.setLineDash([5, 4]);
      ctxF.beginPath();
      ctxF.arc(cx, cy, st.dStab * scale, 0, Math.PI * 2);
      ctxF.stroke();
      ctxF.restore();

      // Draw projected CoM shift under table tilt theta_table along the exact steepest direction (dirX, dirY)
      const shift = st.hHalf * Math.tan(tiltRad);
      const comX = cx + (gem.c0[0] + shift * dirX) * scale;
      const comY = cy - (gem.c0[1] + shift * dirY) * scale;

      drawArrow2D(ctxF, cx, cy, comX, comY, "#d91b42", 2.6, 8);
      ctxF.fillStyle = "#d91b42";
      ctxF.beginPath();
      ctxF.arc(comX, comY, 6, 0, Math.PI * 2);
      ctxF.fill();

      ctxF.font = "bold 11.5px -apple-system, sans-serif";
      ctxF.fillStyle = "#0f6b52";
      ctxF.fillText("■ Centred Support Polygon (Vertices at (0,0) centroid)", 14, HF - 25);
      ctxF.fillStyle = "#b86b00";
      ctxF.fillText("◌ Inscribed Stability Margin d_stab = " + st.dStab.toFixed(4), 14, HF - 9);
      ctxF.fillStyle = "#d91b42";
      ctxF.fillText("● Projected CoM under Tilt θ = " + state.tiltDeg.toFixed(1) + "°", 295, HF - 9);

      // Update readout showing both single-block facet tipping and inclined-joint friction limit
      readout.innerHTML =
        "<span>Contact Polygon: <span class='hl'>A_xy = " + meta.area.toFixed(2) + ", d_stab = " + st.dStab.toFixed(4) + "</span></span>" +
        "<span>1-Block Tipping θ_tip^(1)(λ=" + state.lambda.toFixed(2) + ") = <span class='hl'>" + st.critDeg.toFixed(2) + "°</span> · Joint Friction μ_s ≥ <span class='hl'>" + st.jointTan.toFixed(2) + "</span> (θ_joint = " + st.jointDeg.toFixed(2) + "°)</span>" +
        "<span>Status: <span class='" + (st.toppled ? "warn" : "hl") + "'>" +
        (st.mismatched
          ? "MISMATCHED SLOPES (n_- ≠ -n_+) — Requires Mirror Twin"
          : (st.toppled ? "TOPPLED (θ_table > θ_tip^(1))" : "STATICALLY STABLE (100% Polygon Lock)")) +
        "</span></span>";
    }

    sqSelect.addEventListener("change", function () {
      state.sqKey = sqSelect.value;
      state.topplePhase = 0;
      renderSim4();
    });
    modeSelect.addEventListener("change", function () {
      state.mode = modeSelect.value;
      state.topplePhase = 0;
      renderSim4();
    });
    lamSlider.addEventListener("input", function () {
      state.lambda = parseFloat(lamSlider.value);
      lamVal.textContent = state.lambda.toFixed(2);
      renderSim4();
    });
    tiltSlider.addEventListener("input", function () {
      state.tiltDeg = parseFloat(tiltSlider.value);
      tiltVal.textContent = state.tiltDeg.toFixed(1) + "°";
      renderSim4();
    });
    btnZero.addEventListener("click", function () {
      state.tiltDeg = 0.0;
      state.topplePhase = 0;
      tiltSlider.value = "0.0";
      tiltVal.textContent = "0.0°";
      renderSim4();
    });
    function setTilt(v) {
      state.tiltDeg = v;
      tiltSlider.value = v.toFixed(1);
      tiltVal.textContent = v.toFixed(1) + "°";
    }
    function tweenTilt(to, dur) {
      state.tiltAnim = { from: state.tiltDeg, to: to, t0: performance.now(), dur: dur || 1400 };
    }
    btnCrit.addEventListener("click", function () {
      const st = getTowerStatus();
      state.topplePhase = 0;
      tweenTilt(Math.max(0, st.critDeg - 1.2), 1600);
    });
    btnTopple.addEventListener("click", function () {
      const st = getTowerStatus();
      tweenTilt(Math.min(48.0, st.critDeg + 4.0), 1400);
    });
    tiltSlider.addEventListener("input", function () { state.tiltAnim = null; });
    btnZero.addEventListener("click", function () { state.tiltAnim = null; });
    if (btnLens) {
      btnLens.addEventListener("click", function () {
        state.showLens = !state.showLens;
        btnLens.classList.toggle("active", state.showLens);
        renderSim4();
      });
    }
    function assemble() {
      state.topplePhase = 0;
      state.dropPhase = 0;
    }
    const btnAssemble = document.getElementById("btn-stack-assemble");
    if (btnAssemble) btnAssemble.addEventListener("click", assemble);
    sqSelect.addEventListener("change", assemble);
    modeSelect.addEventListener("change", assemble);
    watchVisibility("sim-stacking");

    window.MG_SIM4 = {
      load: function (o) {
        o = o || {};
        if (o.sq) { state.sqKey = String(o.sq); sqSelect.value = state.sqKey; }
        if (o.mode) { state.mode = o.mode; modeSelect.value = o.mode; }
        state.tiltAnim = null;
        setTilt(0);
        state.topplePhase = 0;
        if (o.assemble !== false) state.dropPhase = 0;
        renderSim4();
      },
      preset: function (name) {
        if (name === "twin-lock") this.load({ sq: "763", mode: "twin" });
        else if (name === "same-fail") this.load({ sq: "763", mode: "same" });
        else if (name === "tilt-test") {
          this.load({ sq: "763", mode: "twin", assemble: false });
          tweenTilt(Math.min(48.0, getTowerStatus().critDeg + 4.0), 4200);
        }
      }
    };

    function tickSim4() {
      let need = false;
      if (state.dropPhase < 4) {
        state.dropPhase = Math.min(4, state.dropPhase + 0.03);
        need = true;
      }
      if (state.tiltAnim) {
        const a = state.tiltAnim;
        const t = Math.min(1, (performance.now() - a.t0) / a.dur);
        setTilt(a.from + (a.to - a.from) * easeInOut(t));
        if (t >= 1) state.tiltAnim = null;
        need = true;
      }
      const st = getTowerStatus();
      if (st.toppled && state.dropPhase >= 4) {
        if (state.topplePhase < 1.6) {
          state.topplePhase = Math.min(1.6, state.topplePhase + 0.035);
          need = true;
        }
      } else if (!st.toppled && state.topplePhase > 0) {
        state.topplePhase = 0;
        need = true;
      }
      if (need && isVisible("sim-stacking")) renderSim4();
      requestAnimationFrame(tickSim4);
    }
    renderSim4();
    requestAnimationFrame(tickSim4);
  }

  // =========================================================================
  // Shared animation helpers & visibility tracking
  // =========================================================================
  const VISIBLE = {};
  function watchVisibility(id) {
    const el = document.getElementById(id);
    if (!el || VISIBLE[id] !== undefined) return;
    VISIBLE[id] = true;
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (e) { VISIBLE[id] = e.isIntersecting; });
      }, { rootMargin: "120px" }).observe(el);
    }
  }
  function isVisible(id) { return VISIBLE[id] !== false; }
  function easeInOut(t) { return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }
  function easeOutBounce(x) {
    const n1 = 7.5625, d1 = 2.75;
    if (x < 1 / d1) return n1 * x * x;
    if (x < 2 / d1) { x -= 1.5 / d1; return n1 * x * x + 0.75; }
    if (x < 2.5 / d1) { x -= 2.25 / d1; return n1 * x * x + 0.9375; }
    x -= 2.625 / d1;
    return n1 * x * x + 0.984375;
  }

  // =========================================================================
  // PLAYGROUND 0: From 4x4 Magic Square to 3D Vectors & Convex Gem
  // =========================================================================
  function initSimIntro() {
    const sel = document.getElementById("intro-sq-select");
    const lamSlider = document.getElementById("intro-lam-slider");
    const lamVal = document.getElementById("intro-lam-val");
    const btnFlat = document.getElementById("btn-intro-flat");
    const btnCube = document.getElementById("btn-intro-cube");
    const btnAnim = document.getElementById("btn-intro-animate");
    const btnPhase2 = document.getElementById("btn-intro-phase2");
    const btnVec = document.getElementById("btn-intro-vectors");
    const btnHull = document.getElementById("btn-intro-hull");
    const btnCore = document.getElementById("btn-intro-core");
    const gridEl = document.getElementById("intro-magic-grid");
    const boardLabel = document.getElementById("intro-board-label");
    const canvas = document.getElementById("canvas-intro-3d");
    const readout = document.getElementById("intro-readout");
    if (!canvas || !gridEl || !sel) return;

    const ctx = canvas.getContext("2d");
    const cam = { yaw: -0.62, pitch: 0.48 };
    const NAMES = {
      "175": "Dürer's Square", "70": "Pell Champion", "46": "Dzhanibekov Champion",
      "673": "Diamond-in-a-Diamond", "763": "Knight's-Move Tower Gem"
    };
    const CORE_DIM = { 0: "a single trapped point", 1: "a trapped segment", 2: "a flat trapped polygon", 3: "a 3D inner core gem" };
    const state = {
      sqKey: sel.value || "175",
      lambda: parseFloat(lamSlider.value) || 0.20,
      showVec: true, showHull: true, showCore: true,
      hover: -1, anim: null, lastInteract: 0, dirty: true, tips: []
    };
    watchVisibility("sim-intro");
    attachOrbitControl(canvas, cam, function () { state.lastInteract = performance.now(); state.dirty = true; });

    function gem() { return GEMS[state.sqKey] || GEMS["175"]; }
    function cellColor(z) {
      const a = 0.14 + 0.55 * Math.abs(z) / 7.5;
      return z > 0 ? "rgba(217,95,2," + a.toFixed(3) + ")" : "rgba(0,114,178," + a.toFixed(3) + ")";
    }

    function setHover(k) {
      state.hover = k;
      Array.prototype.forEach.call(gridEl.children, function (c, idx) { c.classList.toggle("active", idx === k); });
      state.dirty = true;
    }

    function buildGrid() {
      const g = gem();
      const inner = new Set(g.inner_idx);
      gridEl.innerHTML = "";
      for (let k = 0; k < 16; k++) {
        const i = Math.floor(k / 4), j = k % 4, s = g.S[i][j], z = s - 8.5;
        const cell = document.createElement("div");
        cell.className = "mg-cell";
        cell.style.background = cellColor(z);
        if (inner.has(k)) {
          cell.style.borderColor = "#d97706";
          cell.style.boxShadow = "inset 0 0 0 1px #fbbf24";
        }
        cell.innerHTML =
          '<span class="s-num">' + s + '</span>' +
          '<span class="z-num">z=' + (z > 0 ? "+" : "") + z + '</span>' +
          '<span class="ring-dot" style="background:' + RING_COLORS[GRID_XY[k].ring] + '"></span>';
        cell.title = "Number " + s + " → height z = " + z + (inner.has(k) ? " (trapped inside the gem)" : " (outer corner of the gem)");
        cell.addEventListener("mouseenter", function () { setHover(k); });
        cell.addEventListener("mouseleave", function () { setHover(-1); });
        gridEl.appendChild(cell);
      }
      if (boardLabel) boardLabel.textContent = "Square #" + g.idx1 + (NAMES[state.sqKey] ? " (" + NAMES[state.sqKey] + ")" : "");
      state.dirty = true;
    }

    function render() {
      const g = gem();
      const W = canvas.width, H = canvas.height, lam = state.lambda;
      ctx.clearRect(0, 0, W, H);
      // Phase 1 (0 <= lam <= 0.25): keep axis scale COMPLETELY FIXED so the 4x4 floor board
      // never shrinks and each dot lifts straight up/down from its exact 2D square cell to
      // its cubic lift position! Only in Phase 2 (lam > 0.25) zoom out smoothly to fit tall lifts.
      const scale = lam <= 0.25 ? 58.0 : 58.0 / (1.0 + 1.15 * (lam - 0.25));
      const P = function (pt) { return project3D(pt, cam, W, H, scale); };
      const pts = g.P_real.map(function (p) { return [p[0], p[1], p[2] * lam]; });
      const inner = new Set(g.inner_idx);

      // Floor board (4x4 cells in [-2, 2] x [-2, 2])
      const fc = [[-2, -2, 0], [2, -2, 0], [2, 2, 0], [-2, 2, 0]].map(P);
      ctx.fillStyle = "rgba(15, 118, 110, 0.06)";
      ctx.beginPath();
      fc.forEach(function (p, i) { if (i === 0) ctx.moveTo(p.x, p.y); else ctx.lineTo(p.x, p.y); });
      ctx.closePath();
      ctx.fill();
      ctx.strokeStyle = "rgba(120, 140, 132, 0.42)";
      ctx.lineWidth = 1;
      for (let t = -2; t <= 2; t++) {
        let a = P([-2, t, 0]), b = P([2, t, 0]);
        ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
        a = P([t, -2, 0]); b = P([t, 2, 0]);
        ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
      }

      // If near the cubic/square lift (0.12 <= lam <= 0.25), draw the reference [-1.5, 1.5]^3 bounding cube wireframe
      if (lam >= 0.08 && lam <= 0.26) {
        const hz = 7.5 * 0.20; // = 1.50 (exact cube half-height at lam = 0.20)
        const cVerts = [
          [-1.5, -1.5, -hz], [1.5, -1.5, -hz], [1.5, 1.5, -hz], [-1.5, 1.5, -hz],
          [-1.5, -1.5,  hz], [1.5, -1.5,  hz], [1.5, 1.5,  hz], [-1.5, 1.5,  hz]
        ].map(P);
        const cEdges = [
          [0,1],[1,2],[2,3],[3,0], [4,5],[5,6],[6,7],[7,4], [0,4],[1,5],[2,6],[3,7]
        ];
        ctx.save();
        const isExactCube = Math.abs(lam - 0.20) < 0.015;
        ctx.strokeStyle = isExactCube ? "rgba(217, 119, 6, 0.55)" : "rgba(120, 140, 132, 0.25)";
        ctx.lineWidth = isExactCube ? 1.4 : 1;
        ctx.setLineDash([4, 4]);
        cEdges.forEach(function (e) {
          ctx.beginPath();
          ctx.moveTo(cVerts[e[0]].x, cVerts[e[0]].y);
          ctx.lineTo(cVerts[e[1]].x, cVerts[e[1]].y);
          ctx.stroke();
        });
        ctx.restore();
      }

      // Draw 2D start dots (footprints at z = 0) and vertical lift tracks so it is unmistakable where each dot starts and ends
      pts.forEach(function (p, k) {
        const pf = P([p[0], p[1], 0]);
        const pp = P(p);
        const up = g.P_real[k][2] > 0;
        const hov = k === state.hover;
        // Start dot on the flat 4x4 board (z = 0)
        ctx.save();
        ctx.fillStyle = up ? "rgba(217, 95, 2, 0.35)" : "rgba(0, 114, 178, 0.35)";
        ctx.strokeStyle = up ? "rgba(217, 95, 2, 0.75)" : "rgba(0, 114, 178, 0.75)";
        ctx.lineWidth = hov ? 2 : 1;
        ctx.beginPath();
        ctx.arc(pf.x, pf.y, hov ? 4.5 : 2.8, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
        // Vertical lift pillar from z = 0 to z = lam * z_ij
        if (lam > 0.003) {
          ctx.strokeStyle = up
            ? (hov ? "rgba(217, 95, 2, 0.95)" : "rgba(217, 95, 2, 0.52)")
            : (hov ? "rgba(0, 114, 178, 0.95)" : "rgba(0, 114, 178, 0.52)");
          ctx.lineWidth = hov ? 2.4 : 1.35;
          ctx.setLineDash([3, 2.5]);
          ctx.beginPath();
          ctx.moveTo(pf.x, pf.y);
          ctx.lineTo(pp.x, pp.y);
          ctx.stroke();
        }
        ctx.restore();
      });

      // Hull faces sorted far-to-near; back faces drawn before vectors, front faces after
      const faces = g.faces0.map(function (f) {
        const fp = f.verts.map(function (v) { return pts[v]; });
        let c = [0, 0, 0];
        fp.forEach(function (p) { c = vecAdd(c, p); });
        return { fp: fp, d: P(vecScale(c, 1 / fp.length)).depth };
      }).sort(function (a, b) { return a.d - b.d; });
      function drawFace(f, front) {
        ctx.fillStyle = front ? "rgba(15, 118, 110, 0.13)" : "rgba(15, 118, 110, 0.07)";
        ctx.strokeStyle = front ? "rgba(15, 118, 110, 0.75)" : "rgba(15, 118, 110, 0.28)";
        ctx.lineWidth = front ? 1.3 : 1;
        ctx.beginPath();
        f.fp.forEach(function (p, i) { const q = P(p); if (i === 0) ctx.moveTo(q.x, q.y); else ctx.lineTo(q.x, q.y); });
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
      }
      if (state.showHull && lam > 0.005) faces.filter(function (f) { return f.d < 0; }).forEach(function (f) { drawFace(f, false); });

      // Inner core
      if (state.showCore && g.inner_idx.length > 1 && lam > 0.005) {
        if (g.rk1 === 3 && g.faces1 && g.faces1.length) {
          g.faces1.map(function (tri) {
            const tp = tri.map(function (vi) { return pts[vi]; });
            let c = [0, 0, 0];
            tp.forEach(function (p) { c = vecAdd(c, p); });
            return { tp: tp, d: P(vecScale(c, 1 / 3)).depth };
          }).sort(function (a, b) { return a.d - b.d; }).forEach(function (f) {
            ctx.fillStyle = "rgba(217, 119, 6, 0.32)";
            ctx.strokeStyle = "#b45309";
            ctx.lineWidth = 1.1;
            ctx.beginPath();
            f.tp.forEach(function (p, i) { const q = P(p); if (i === 0) ctx.moveTo(q.x, q.y); else ctx.lineTo(q.x, q.y); });
            ctx.closePath();
            ctx.fill();
            ctx.stroke();
          });
        } else {
          const ip = g.inner_idx.map(function (vi) { return pts[vi]; });
          let c = [0, 0, 0];
          ip.forEach(function (p) { c = vecAdd(c, p); });
          c = vecScale(c, 1 / ip.length);
          ip.sort(function (a, b) { return Math.atan2(a[1] - c[1], a[0] - c[0]) - Math.atan2(b[1] - c[1], b[0] - c[0]); });
          ctx.fillStyle = "rgba(217, 119, 6, 0.25)";
          ctx.strokeStyle = "#b45309";
          ctx.lineWidth = 1.6;
          ctx.beginPath();
          ip.forEach(function (p, i) { const q = P(p); if (i === 0) ctx.moveTo(q.x, q.y); else ctx.lineTo(q.x, q.y); });
          ctx.closePath();
          ctx.fill();
          ctx.stroke();
        }
      }

      // 16 vectors from O
      const pO = P([0, 0, 0]);
      const order = pts.map(function (p, k) { return { k: k, d: P(p).depth }; }).sort(function (a, b) { return a.d - b.d; });
      if (state.showVec) {
        order.forEach(function (o) {
          const p = pts[o.k], pp = P(p);
          const up = g.P_real[o.k][2] > 0;
          const hov = o.k === state.hover;
          ctx.globalAlpha = state.hover >= 0 && !hov ? 0.32 : 0.85;
          drawArrow2D(ctx, pO.x, pO.y, pp.x, pp.y, up ? "#d95f02" : "#0072b2", hov ? 3.4 : 1.5, hov ? 9 : 6);
          ctx.globalAlpha = 1;
        });
      }
      if (state.showHull && lam > 0.005) faces.filter(function (f) { return f.d >= 0; }).forEach(function (f) { drawFace(f, true); });

      // Tips + labels
      state.tips = [];
      order.forEach(function (o) {
        const k = o.k, pp = P(pts[k]);
        const s = g.S[Math.floor(k / 4)][k % 4];
        const up = g.P_real[k][2] > 0;
        const hov = k === state.hover;
        const r = hov ? 8 : 4.8;
        ctx.save();
        if (hov) { ctx.shadowColor = up ? "#fb923c" : "#38bdf8"; ctx.shadowBlur = 14; }
        ctx.fillStyle = up ? "#d95f02" : "#0072b2";
        ctx.beginPath(); ctx.arc(pp.x, pp.y, r, 0, Math.PI * 2); ctx.fill();
        ctx.restore();
        if (inner.has(k)) {
          ctx.strokeStyle = "#f59e0b";
          ctx.lineWidth = 2.2;
          ctx.beginPath(); ctx.arc(pp.x, pp.y, r + 2.5, 0, Math.PI * 2); ctx.stroke();
        }
        ctx.fillStyle = "#182224";
        ctx.font = (hov ? "bold 13px" : "bold 10.5px") + " -apple-system, sans-serif";
        ctx.fillText(String(s), pp.x + r + 2, pp.y - 3);
        state.tips.push({ k: k, x: pp.x, y: pp.y });
      });

      ctx.fillStyle = "#111";
      ctx.beginPath(); ctx.arc(pO.x, pO.y, 4, 0, Math.PI * 2); ctx.fill();
      ctx.font = "bold 11px -apple-system, sans-serif";
      ctx.fillText("O", pO.x - 14, pO.y + 4);

      // Caption showing current phase
      ctx.fillStyle = "#132a2c";
      ctx.font = "bold 12.5px -apple-system, sans-serif";
      let phaseTitle = "λ = " + lam.toFixed(2) + ": numbers lifted into 3D";
      if (lam < 0.01) {
        phaseTitle = "Start (λ = 0.00): Flat 4×4 board — all 16 dots sit on their grid cells";
      } else if (Math.abs(lam - 0.20) < 0.012) {
        phaseTitle = "Phase 1 Stop (λ = 0.20): Cubic Lift — height ±1.5 matches 3×3 board width (fixed axes)";
      } else if (lam < 0.20) {
        phaseTitle = "Phase 1 (λ = " + lam.toFixed(2) + " → 0.20): Lifting dots straight from 2D cells (axes fixed)";
      } else if (lam > 0.20) {
        phaseTitle = "Phase 2 (λ = " + lam.toFixed(2) + "): Stretching vertical lift past the cube (I⊥/I_zz = " + (0.5 * (1 + 17 * lam * lam)).toFixed(2) + ")";
      }
      ctx.fillText(phaseTitle, 14, 22);
      if (state.hover >= 0) {
        const k = state.hover, p = pts[k], s = g.S[Math.floor(k / 4)][k % 4];
        const txt = "Number " + s + ": starts at (" + p[0].toFixed(1) + ", " + p[1].toFixed(1) + ", 0) → lifts to (" + p[0].toFixed(1) + ", " + p[1].toFixed(1) + ", " + p[2].toFixed(2) + ")" + (inner.has(k) ? " · trapped inside" : " · outer corner");
        ctx.font = "12px -apple-system, sans-serif";
        const tw = ctx.measureText(txt).width;
        ctx.fillStyle = "rgba(16, 33, 36, 0.92)";
        ctx.fillRect(12, H - 38, tw + 18, 26);
        ctx.fillStyle = "#ffffff";
        ctx.fillText(txt, 21, H - 20);
      } else {
        ctx.fillStyle = "#5c696d";
        ctx.font = "11px -apple-system, sans-serif";
        ctx.fillText(
          lam <= 0.25
            ? "Phase 1: axes locked at 1:1 scale so each dot's 2D start → 3D end track is exact"
            : "Phase 2: stretching λ changes aspect & inertia ratio I⊥/I_zz = (1 + 17λ²)/2",
          14, H - 14
        );
      }

      // Readout
      let sum = [0, 0, 0];
      pts.forEach(function (p) { sum = vecAdd(sum, p); });
      const f = g.f_vector;
      const ratioI = 0.5 * (1 + 17 * lam * lam);
      readout.innerHTML =
        "<span>Vector Sum: <span class='hl'>(" + sum.map(function (v) { return (Math.abs(v) < 1e-9 ? 0 : v).toFixed(2); }).join(", ") + ")</span> · Max height ±" + (7.5 * lam).toFixed(2) + "</span>" +
        "<span>Inertia ratio I⊥ / I_zz: <span class='hl'>" + ratioI.toFixed(2) + (Math.abs(lam - 0.20) < 0.01 ? " (Cubic 0.84)" : (Math.abs(lam - 1 / Math.sqrt(17)) < 0.01 ? " (Spherical Top 1.00)" : "")) + "</span></span>" +
        "<span>Hull: <span class='hl'>" + f[0] + " corners, " + f[2] + " faces</span> · Core: <span class='gold'>" + g.inner_idx.length + " trapped</span></span>";
    }

    function updatePresetButtons() {
      if (btnFlat) btnFlat.classList.toggle("active", Math.abs(state.lambda) < 0.008);
      if (btnCube) btnCube.classList.toggle("active", Math.abs(state.lambda - 0.20) < 0.008);
    }

    function setLam(v) {
      state.lambda = v;
      lamSlider.value = v.toFixed(2);
      lamVal.textContent = v.toFixed(2);
      updatePresetButtons();
      state.dirty = true;
    }

    sel.addEventListener("change", function () { state.sqKey = sel.value; setHover(-1); buildGrid(); });
    lamSlider.addEventListener("input", function () { state.anim = null; setLam(parseFloat(lamSlider.value)); });
    if (btnFlat) {
      btnFlat.addEventListener("click", function () {
        state.anim = null;
        setLam(0.0);
      });
    }
    if (btnCube) {
      btnCube.addEventListener("click", function () {
        state.anim = null;
        setLam(0.20);
      });
    }
    // Phase 1 button: animate from flat 2D (lam = 0) and STOP at the cubic/square lift (lam = 0.20)
    // with camera & axis dimensions completely fixed so the user clearly sees each dot's start & end
    btnAnim.addEventListener("click", function () {
      state.lastInteract = performance.now(); // pause auto-orbit during the lift so dots go straight up/down
      setLam(0);
      state.anim = { from: 0, to: 0.20, t0: performance.now() + 200, dur: 2200 };
    });
    // Phase 2 button: lift further from the cubic lift (lam = 0.20) out to lam = 1.0 (and back to 0.20 if clicked at 1.0)
    if (btnPhase2) {
      btnPhase2.addEventListener("click", function () {
        state.lastInteract = performance.now();
        const startLam = (state.lambda < 0.18 || state.lambda > 0.92) ? 0.20 : state.lambda;
        setLam(startLam);
        state.anim = { from: startLam, to: 1.00, t0: performance.now() + 150, dur: 2800 };
      });
    }
    [[btnVec, "showVec"], [btnHull, "showHull"], [btnCore, "showCore"]].forEach(function (pair) {
      if (!pair[0]) return;
      pair[0].addEventListener("click", function () {
        state[pair[1]] = !state[pair[1]];
        pair[0].classList.toggle("active", state[pair[1]]);
        state.dirty = true;
      });
    });
    canvas.addEventListener("mousemove", function (e) {
      if (e.buttons) return;
      const rect = canvas.getBoundingClientRect();
      const mx = (e.clientX - rect.left) * (canvas.width / rect.width);
      const my = (e.clientY - rect.top) * (canvas.height / rect.height);
      let best = -1, bd = 14;
      state.tips.forEach(function (t) {
        const d = Math.hypot(t.x - mx, t.y - my);
        if (d < bd) { bd = d; best = t.k; }
      });
      if (best !== state.hover) setHover(best);
    });
    canvas.addEventListener("mouseleave", function () { setHover(-1); });

    function frame(now) {
      if (state.anim && now >= state.anim.t0) {
        state.lastInteract = now; // keep camera steady while lifting
        const t = Math.min(1, (now - state.anim.t0) / state.anim.dur);
        setLam(state.anim.from + (state.anim.to - state.anim.from) * easeInOut(t));
        if (t >= 1) state.anim = null;
      }
      if (isVisible("sim-intro") && !state.anim && now - state.lastInteract > 3200 && state.hover < 0) {
        cam.yaw += 0.003;
        state.dirty = true;
      }
      if (state.dirty && isVisible("sim-intro")) {
        render();
        state.dirty = false;
      }
      requestAnimationFrame(frame);
    }
    buildGrid();
    updatePresetButtons();
    requestAnimationFrame(frame);
  }

  // =========================================================================
  // Page glue: story cards, census jump chips, and table-of-contents highlight
  // =========================================================================
  function scrollToCard(id) {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  function initGlue() {
    [["data-sim1-preset", "sim-rings", "MG_SIM1"],
     ["data-sim2-preset", "sim-precession", "MG_SIM2"],
     ["data-sim3-preset", "sim-nested", "MG_SIM3"],
     ["data-sim4-preset", "sim-stacking", "MG_SIM4"],
     ["data-fab-preset", "sim-fab", "MG_SIM_FAB"]].forEach(function (cfg) {
      document.querySelectorAll("[" + cfg[0] + "]").forEach(function (btn) {
        btn.addEventListener("click", function () {
          scrollToCard(cfg[1]);
          const name = btn.getAttribute(cfg[0]);
          setTimeout(function () { if (window[cfg[2]]) window[cfg[2]].preset(name); }, 350);
        });
      });
    });

    const SIM_IDS = { "1": "sim-rings", "2": "sim-precession", "3": "sim-nested", "4": "sim-stacking", "fab": "sim-fab" };
    document.querySelectorAll("[data-jump-sim]").forEach(function (a) {
      a.addEventListener("click", function (e) {
        e.preventDefault();
        const n = a.getAttribute("data-jump-sim");
        const d = a.dataset;
        scrollToCard(SIM_IDS[n]);
        setTimeout(function () {
          if (n === "1" && window.MG_SIM1) {
            window.MG_SIM1.load({
              sq: d.sq,
              alpha: d.alpha !== undefined ? parseFloat(d.alpha) : undefined,
              view: d.view || (d.alpha !== undefined ? "polygon" : undefined),
              weights: d.weights === "1"
            });
          } else if (n === "2" && window.MG_SIM2) {
            window.MG_SIM2.load({ sq: d.sq, model: d.model, kick: "dzh" });
          } else if (n === "3" && window.MG_SIM3) {
            window.MG_SIM3.load({ sq: d.sq, snap: d.snap === "1" });
          } else if (n === "fab" && window.MG_SIM_FAB) {
            window.MG_SIM_FAB.load({
              sq: d.sq,
              lam: d.lam !== undefined ? parseFloat(d.lam) : (d.right === "paper" ? 0.20 : 1.00),
              fab: d.fab,
              right: d.right,
              snap: d.snap === "1"
            });
          } else if (n === "4" && window.MG_SIM4) {
            window.MG_SIM4.load({ sq: d.sq, mode: d.mode });
          }
        }, 400);
      });
    });

    const links = Array.prototype.slice.call(document.querySelectorAll("nav.d-toc a"));
    if ("IntersectionObserver" in window && links.length) {
      const io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          links.forEach(function (l) { l.classList.toggle("active", l.getAttribute("href") === "#" + e.target.id); });
        });
      }, { rootMargin: "-35% 0px -60% 0px" });
      document.querySelectorAll("main.d-article section[id]").forEach(function (s) { io.observe(s); });
    }
  }

  // Initialize all 6 interactive simulators and page glue on DOM ready
  function initAll() {
    initSimIntro();
    initSim1();
    initSim2();
    initSim3();
    initSimFab();
    initSim4();
    initGlue();
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAll);
  } else {
    initAll();
  }
})();
