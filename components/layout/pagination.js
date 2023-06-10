function Pagination({ totalPosts, postsPerpage, setCurrentPage, currentPage }) {
  let pages = [];

  for (let i = 1; i <= Math.ceil(totalPosts / 3); i++) {
    pages.push(i);
  }

  return (
    <div>
      {pages.map((page, index) => {
        return (
          <button
            key={index}
            className={
              page == currentPage
                ? "btn btn-success active m-1  "
                : "btn btn-success m-1"
            }
            onClick={() => setCurrentPage(page)}
          >
            {page}
          </button>
        );
      })}
    </div>
  );
}

export default Pagination;
