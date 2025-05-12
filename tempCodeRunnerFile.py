    if upgrade_button.draw(screen):
            if world.money >= cost_to_upgrade_selected_turret:
              selected_turret.upgrade()
              world.money -= cost_to_upgrade_selected_turret