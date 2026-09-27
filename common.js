document.addEventListener("DOMContentLoaded", () => {

    /*
     * GitHub Pages 기준
     *
     * 예:
     * /mil/index.html
     * /mil/칼럼/전체 데이터.html
     * /mil/부대분류/부대분류/조회사이트.html
     *
     * 모두 /mil/ 을 기준으로 이동
     */

    const path = window.location.pathname;

    const milIndex = path.indexOf("/mil/");

    const root =
        milIndex !== -1
            ? path.substring(0, milIndex + 5)
            : "/";


    /* =========================
       HEADER
    ========================= */

    const header =
        document.getElementById("common-header");


    if (header) {

        header.innerHTML = `
            <header class="site-header">

                <div class="site-header-inner">

                    <a
                        class="site-logo"
                        href="${root}index.html"
                    >
                        🪖 군무원 배정정보
                    </a>


                    <nav class="site-nav">

                        <a href="${root}index.html">
                            홈
                        </a>

                        <a href="${root}부대분류/부대분류/조회사이트.html">
                            9급
                        </a>

                        <a href="${root}부대분류/부대분류/칼럼/678급.html">
                            7급
                        </a>

                        <a href="${root}부대분류/부대분류/칼럼/QNA.html">
                            QNA
                        </a>

                    </nav>

                </div>

            </header>
        `;

    }



    /* =========================
       FOOTER
    ========================= */

    const footer =
        document.getElementById("common-footer");


    if (footer) {

        footer.innerHTML = `
            <footer class="site-footer">

                <div class="site-footer-inner">

                    <div class="footer-title">
                        군무원 배정정보
                    </div>

                    <div class="footer-text">
                         ㆍ육통이ㆍ
                    </div>

                    <div class="footer-notice">
                        본 사이트의 데이터는 참고용이며
                        실제 인사 결과와 다를 수 있습니다.
                    </div>

                </div>

            </footer>
        `;

    }

});