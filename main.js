/* NEXUS採用LP — 最小限のJS
   ・追従CTAバーの表示制御（ファーストビュー内では隠す）
   ・勤務地のエリアタブ切り替え
   JSが動かない場合でも、バーは常時表示、店舗は全エリア表示になるだけで機能は落ちません。 */

(function () {
  'use strict';

  /* ---------- 追従CTAバー ---------- */
  var bar = document.getElementById('bar');
  var hero = document.getElementById('hero');

  if (bar && hero && 'IntersectionObserver' in window) {
    // ヒーローが見えている間は隠す（ヒーロー自体にCTAが2つあるため）
    bar.classList.add('is-off');
    new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        bar.classList.toggle('is-off', e.isIntersecting);
      });
    }, { threshold: 0.15 }).observe(hero);
  }

  /* ---------- エリアタブ ---------- */
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.tab[data-area]'));
  var panels = Array.prototype.slice.call(document.querySelectorAll('.area-panel[data-area]'));

  if (tabs.length && panels.length) {
    var show = function (area) {
      tabs.forEach(function (t) {
        t.setAttribute('aria-selected', String(t.dataset.area === area));
      });
      panels.forEach(function (pnl) {
        pnl.hidden = pnl.dataset.area !== area;
      });
    };

    // 初期表示：最初のエリアだけ
    show(tabs[0].dataset.area);

    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { show(t.dataset.area); });
      // 左右キーでタブ移動
      t.addEventListener('keydown', function (ev) {
        var d = ev.key === 'ArrowRight' ? 1 : ev.key === 'ArrowLeft' ? -1 : 0;
        if (!d) return;
        ev.preventDefault();
        var next = tabs[(i + d + tabs.length) % tabs.length];
        next.focus();
        show(next.dataset.area);
      });
    });
  }

  /* ---------- CTAクリックの計測 ----------
     GTMのカスタムイベントトリガー「cta_click」で拾えます。
     どのボタンが押されたかは cta_id で判別できます。 */
  window.dataLayer = window.dataLayer || [];
  document.addEventListener('click', function (ev) {
    var el = ev.target.closest ? ev.target.closest('[data-cta]') : null;
    if (!el) return;
    window.dataLayer.push({ event: 'cta_click', cta_id: el.dataset.cta });
  });
})();
