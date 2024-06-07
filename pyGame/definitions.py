def show_leads(field, leaderboard_labels):
    for i in range(5):
        field.blit(leaderboard_labels[i], (450, 100 + (i * 40)))


def config_leads(db_manager, nickname, score_to_ins, leaderboard_labels, font):
    db_manager.write_score(nickname, score_to_ins)
    top_players = db_manager.get_top_players()
    for ranking, player in enumerate(top_players, start=1):
        leaderboard_labels[ranking - 1] = font.render(
            f'{ranking}.{player[0]}, Score: {player[1]}', False, (168, 2, 2))


def menu_win(field, menu_bg, restart_label, restart_label_rect, name, description, leads_label):
    field.blit(menu_bg, (0, 0))
    field.blit(restart_label, restart_label_rect)
    field.blit(name, (65, 40))
    field.blit(description, (65, 80))

    field.blit(leads_label, (385, 35))


def menu_start(field, menu_bg, restart_label, restart_label_rect, name, description, description2, leads_label):
    field.blit(menu_bg, (0, 0))
    field.blit(restart_label, restart_label_rect)
    field.blit(name, (65, 40))
    field.blit(description, (65, 80))
    field.blit(description2, (65, 200))

    field.blit(leads_label, (385, 35))


def menu_loss(field, menu_bg, restart_label, restart_label_rect, description, lose_label, leads_label):
    field.blit(menu_bg, (0, 0))
    field.blit(lose_label, (65, 35))
    field.blit(restart_label, restart_label_rect)
    field.blit(description, (155, 200))

    field.blit(leads_label, (385, 35))
