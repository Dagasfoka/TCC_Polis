const MATCH_ID_KEY="match_id"
export function saveMatchID(match_id) {
  sessionStorage.setItem(MATCH_ID_KEY, match_id);
}

export function getSavedMatchID() {
  return sessionStorage.getItem(MATCH_ID_KEY);
}

export function clearMatchID() {
  sessionStorage.removeItem(MATCH_ID_KEY);
}