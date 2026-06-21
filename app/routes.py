from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, Player, Match

bp = Blueprint('main', __name__)

#главная страница
@bp.route('/')
def index():
    search_query = request.args.get('search', '')
    
    #поиск игроков по нику
    if search_query:
        players = Player.query.filter(Player.nickname.contains(search_query)).all()
    else:
        #сортировка по очкам
        players = Player.query.order_by(Player.points.desc()).all()
        
    matches = Match.query.order_by(Match.id.desc()).all()
    return render_template('index.html', players=players, matches=matches, search_query=search_query)

#добавление нового игрока
@bp.route('/player/add', methods=['POST'])
def add_player():
    name = request.form.get('name')
    nickname = request.form.get('nickname')
    
    #проверка на пустое поле
    if not name or not nickname:
        flash('Имя и никнейм не могут быть пустыми!')
        return redirect(url_for('main.index'))
        
    #проверка на одинаковые ники
    existing = Player.query.filter_by(nickname=nickname).first()
    if existing:
        flash('Игрок с таким никнеймом уже существует!')
        return redirect(url_for('main.index'))

    new_player = Player(name=name, nickname=nickname, points=0)
    db.session.add(new_player)
    db.session.commit()
    return redirect(url_for('main.index'))

#добавление матча
@bp.route('/match/add', methods=['GET', 'POST'])
def add_match():
    if request.method == 'POST':
        p1_id = request.form.get('player1')
        p2_id = request.form.get('player2')
        winner_id = request.form.get('winner')
        
        if p1_id == p2_id:
            flash('Игрок не может играть сам с собой!')
            return redirect(url_for('main.add_match'))
            
        new_match = Match(player1_id=p1_id, player2_id=p2_id, winner_id=winner_id)
        
        #начисление очка победителю
        winner = Player.query.get(winner_id)
        if winner:
            winner.points += 1
            
        db.session.add(new_match)
        db.session.commit()
        return redirect(url_for('main.index'))
        
    players = Player.query.all()
    return render_template('add_match.html', players=players)

#удаление игрока
@bp.route('/player/delete/<int:player_id>', methods=['POST'])
def delete_player(player_id):
    player = Player.query.get_or_404(player_id)
    db.session.delete(player)
    db.session.commit()
    return redirect(url_for('main.index'))
    
#очистка матчей и обнуление очков
@bp.route('/tournament/reset', methods=['POST'])
def reset_tournament():
    Match.query.delete()
    
    players = Player.query.all()
    for player in players:
        player.points = 0
        
    db.session.commit()
    flash('Турнир успешно сброшен! Очки обнулены, история очищена.')
    return redirect(url_for('main.index'))