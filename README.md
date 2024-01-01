# sutdy-backend-board
study backend for board api

# upgrade board
- 질문에 대한 답변 컨텐츠를 테이블에 넣고 페이징 기능 추가, 답변 테이블을 좋아요(like) 갯수로 정렬 
   - branch : board_x_1

# modifications

### pagination
- answer_list_v2.html 템플릿 생성
   - /question/detail/ 엔드포인트로부터 answer_list.paginate() 객체를 넘겨 받아서 사용 
- 답변 리스트가 보여지는 질문 상세 페이지(question_detail.html)에서 include 함수를 사용하여 answer_list.html을 추가
- 기존에 답변 컨텐츠를 field에 나열하는 방식에서 테이블로 변경
- 테이블에 답변의 갯수가 많아질 경우 페이지가 넘어가도록 페이징 기능 추가
   - 컨텐츠 번호, 페이지 이동 bar, before-next button 등
- 질문 상세 페이지의 데이터를 생성하는 /question/detail/ 엔드포인트에서 답변 리스트 객체를 생성하고 paginate 함수를 적용
   - answer_list = answer_list.paginate(page=page, per_page=5)

### sort by like count
- 답변 테이블을 정렬하기 위해 답변의 좋아요 갯수를 사용
- 답변 상세 엔드포인트(/question/detail/)에서 ORM 명령어를 사용하여 db 설정
- 답변 좋아요 테이블(answer_voter)을 Query() 명령어를 사용하여 subquery()로 설정
   - answer_voter 테이블을 답변 아이디(answer_id) 기준으로 그룹화
   - sqlalchemy의 func 함수의 count 기능을 사용하여 그룹화 된 답변의 갯수 확인
   - .query()에 사용할 컬럼을 설정해야, join 후에 해당 컬럼을 사용할 수 있다.
   - sub_query = db.session.query(av.c.answer_id, func.count(av.c.user_id).label('count')) \
                          .group_by(av.c.answer_id).subquery()
- 답변 리스트 테이블(answer_list)을 생성
   - answer_list = Answer.query.filter(Answer.question_id == question_id)
- 답변 리스트 테이블과 답변 좋아요 서브쿼리를 outerjoin 한 후 정렬
   - answer_list = answer_list.outerjoin(sub_query, sub_query.c.answer_id == Answer.id).order_by(sub_query.c.count.desc())
   - .outerjoin()이 아닌 .join()을 사용하면 left join이 되어 답변 리스트 테이블 기준 좋아요 갯수 값이 없는경우(null) 행이 반환되지 않는다.
