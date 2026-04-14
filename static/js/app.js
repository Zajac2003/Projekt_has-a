const rowsBody = document.getElementById("rowsBody");
const searchInput = document.getElementById("searchInput");
const resetButton = document.getElementById("resetButton");
const totalRows = document.getElementById("totalRows");
const visibleRows = document.getElementById("visibleRows");
const drawer = document.getElementById("drawer");
const drawerTitle = document.getElementById("drawerTitle");
const drawerText = document.getElementById("drawerText");
const drawerCandidate = document.getElementById("drawerCandidate");
const drawerTime = document.getElementById("drawerTime");
const drawerClose = document.getElementById("drawerClose");

let rows = [];
let searchTimer = null;

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function openDrawer(row, result) {
  drawerTitle.textContent = `${row.username} - analiza`;
  drawerText.textContent = result.result;
  drawerCandidate.textContent = result.candidate;
  drawerTime.textContent = result.analysis_time || row.analysis_time || "—";
  drawer.classList.add("visible");
}

function renderRows(list) {
  visibleRows.textContent = list.length;

  if (!list.length) {
    rowsBody.innerHTML = `
      <tr>
        <td colspan="7">
          <div class="empty-state">Brak wyników dla podanego filtra.</div>
        </td>
      </tr>
    `;
    return;
  }

  rowsBody.innerHTML = list
    .map(
      (row) => `
        <tr data-id="${row.id}">
          <td>${row.id}</td>
          <td>
            <strong>${escapeHtml(row.username)}</strong><br />
            <span>${escapeHtml(row.algorithm)}</span>
          </td>
          <td>${escapeHtml(row.email)}</td>
          <td class="mono">${escapeHtml(row.hash)}</td>
          <td><span class="status-pill">${escapeHtml(row.algorithm)}</span></td>
          <td><span class="status-pill">${escapeHtml(row.analysis_time || "—")}</span></td>
          <td><span class="status-pill">${escapeHtml(row.status)}</span></td>
          <td>
            <button class="action-button" type="button" data-action="simulate" data-id="${row.id}">Odszyfruj</button>
          </td>
        </tr>
      `,
    )
    .join("");
}

async function fetchRows(query = "") {
  const response = await fetch(`/api/rows?q=${encodeURIComponent(query)}`);
  rows = await response.json();
  totalRows.textContent = rows.length;
  renderRows(rows);
}

async function simulateRow(id, button) {
  const row = rows.find((item) => item.id === id);
  if (!row) {
    return;
  }

  const previousText = button.textContent;
  button.disabled = true;
  button.dataset.state = "working";
  button.textContent = "Analizuję...";

  try {
    const response = await fetch("/api/simulate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id }),
    });
    const payload = await response.json();
    openDrawer(row, payload);
    button.dataset.state = "done";
    button.textContent = "Wynik gotowy";
  } catch (error) {
    drawerTitle.textContent = "Błąd symulacji";
    drawerText.textContent = "Nie udało się uruchomić symulacji analizy.";
    drawerCandidate.textContent = "—";
    drawerTime.textContent = "—";
    drawer.classList.add("visible");
    button.textContent = previousText;
  } finally {
    button.disabled = false;
  }
}

searchInput.addEventListener("input", () => {
  window.clearTimeout(searchTimer);
  searchTimer = window.setTimeout(() => {
    fetchRows(searchInput.value.trim());
  }, 180);
});

resetButton.addEventListener("click", () => {
  searchInput.value = "";
  fetchRows("");
});

drawerClose.addEventListener("click", () => {
  drawer.classList.remove("visible");
});

rowsBody.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-action='simulate']");
  if (!button) {
    return;
  }

  simulateRow(Number(button.dataset.id), button);
});

fetchRows();