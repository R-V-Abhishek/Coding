def solve_agilans_project():
    import sys

    def read_nonempty():
        s = sys.stdin.readline()
        while s is not None and s.strip() == "":
            s = sys.stdin.readline()
        return s.strip()

    n = int(read_nonempty())
    instr = []
    for _ in range(n):
        d, k = read_nonempty().split()
        instr.append((d, int(k)))
    start_x, start_y = map(int, read_nonempty().split())
    target_x, target_y = map(int, read_nonempty().split())

    turn_to_rot = {"left": -1, "right": 1, "straight": 0, "back": 2}
    rot_norm = { -1: 3, 0: 0, 1: 1, 2: 2 }  # mod 4 normalization for -1
    dirs = [(0,1), (1,0), (0,-1), (-1,0)]  # N,E,S,W

    pref_pos = [(start_x, start_y)] * (n + 1)
    pref_face = [0] * (n + 1)  # 0=N,1=E,2=S,3=W

    for i, (t, dist) in enumerate(instr):
        r = rot_norm[turn_to_rot[t]]
        f = (pref_face[i] + r) % 4
        dx, dy = dirs[f]
        x, y = pref_pos[i]
        pref_pos[i+1] = (x + dx*dist, y + dy*dist)
        pref_face[i+1] = f

    if pref_pos[-1] == (target_x, target_y):
        print("No")
        return

    # Suffix displacement relative to starting facing = North
    suf_disp_rel = [(0,0)] * (n + 1)  # displacement if starting facing = North
    for i in range(n-1, -1, -1):
        t, dist = instr[i]
        r = rot_norm[turn_to_rot[t]]
        f_step = r % 4
        dx_step, dy_step = dirs[f_step]
        step_disp = (dx_step*dist, dy_step*dist)
        dx_rel, dy_rel = suf_disp_rel[i+1]
        # rotate next suffix displacement by r
        if r == 0:
            rot_dx, rot_dy = dx_rel, dy_rel
        elif r == 1:
            rot_dx, rot_dy = dy_rel, -dx_rel
        elif r == 2:
            rot_dx, rot_dy = -dx_rel, -dy_rel
        else:  # r == 3
            rot_dx, rot_dy = -dy_rel, dx_rel
        suf_disp_rel[i] = (step_disp[0] + rot_dx, step_disp[1] + rot_dy)

    candidates = ("left", "right", "straight", "back")

    for i, (orig_turn, dist) in enumerate(instr):
        base_x, base_y = pref_pos[i]
        f_before = pref_face[i]
        for new_turn in candidates:
            if new_turn == orig_turn:
                continue
            r_new = rot_norm[turn_to_rot[new_turn]]
            f_new = (f_before + r_new) % 4
            dx_step, dy_step = dirs[f_new]
            step_disp = (dx_step*dist, dy_step*dist)

            dx_rel, dy_rel = suf_disp_rel[i+1]
            # rotate suffix by f_new
            if f_new == 0:
                rot_dx, rot_dy = dx_rel, dy_rel
            elif f_new == 1:
                rot_dx, rot_dy = dy_rel, -dx_rel
            elif f_new == 2:
                rot_dx, rot_dy = -dx_rel, -dy_rel
            else:
                rot_dx, rot_dy = -dy_rel, dx_rel

            fin_x = base_x + step_disp[0] + rot_dx
            fin_y = base_y + step_disp[1] + rot_dy

            if (fin_x, fin_y) == (target_x, target_y):
                print("Yes")
                print(f"{orig_turn} {dist}")
                print(f"{new_turn} {dist}")
                return

    print("No")


if __name__ == "__main__":
    solve_agilans_project()
