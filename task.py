from tkinter import *
import sqlite3

# Window
root = Tk()
root.title('Task')

root.geometry('500x500')

# Database
con = sqlite3.connect( 'tasks.db' )

cur = con.cursor()

cur.execute('''
    CREATE TABLE if not exists tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        description TEXT NOT NULL,
        completed BOOLEAN NOT NULL
    );
''')
con.commit()

# Functions
def remove_task( id_task ):
    def _remove_task():
        cur.execute('''
            DELETE FROM tasks
            WHERE id = ?
        ''', ( id_task, )
        )
        con.commit()

        cmd_show()
    return _remove_task

def cmd_completed( id_task ):
    def _completed():

        '''
        Completes a task
        '''
        task = cur.execute('''
            SELECT * from tasks WHERE id = ?
        ''', ( id_task, )
        ).fetchone()

        cur.execute('''
            UPDATE tasks
            SET completed = ?
            WHERE id = ?
        ''', ( not task[ 3 ], id_task )
        )
        con.commit()
        cmd_show()
    return _completed

def cmd_show():
    '''
    Shows the task
    '''
    row_task = cur.execute('''
        SELECT * FROM tasks
        '''
    ).fetchall()

    #print(row_task)
    for widget in lbl_frame.winfo_children():
        widget.destroy()

    for item in range(0, len( row_task ) ):
        completed_task = row_task[item][ 3 ]
        description_task = row_task[item][ 2 ]

        id_task = row_task[item][ 0 ]

        color_task = '#555555' if completed_task else '#000000'

        # Check Button
        check_btn = Checkbutton( lbl_frame, text=description_task, width=42, anchor='w', command = cmd_completed(id_task), fg=color_task )
        check_btn.grid( row=item, column=0, sticky='W' )
        check_btn.select() if completed_task else check_btn.deselect

        btn_del = Button( lbl_frame, text='Delete', command=remove_task(id_task) )
        btn_del.grid( row=item, column=1, sticky='W')

def cmd_task():
    '''
    Adds a task
    '''
    task = entry_task.get()

    if task:
        cur.execute('''
            INSERT INTO tasks(
                description,
                completed 
            )
            VALUES(
                ?,
                ?
            )
        ''',
        ( task, False )
        )
        con.commit()

        entry_task.delete(0, END)

        cmd_show()
    else:
        pass

# Label
lbl_tasks = Label( root, text= 'Task', padx=5, pady=5)

lbl_tasks.grid( row=0, column=0, padx=20 )

# Entry
entry_task = Entry( root, width=40 )
entry_task.grid( row=0, column=1, pady=20 )

# Button
btn_task = Button( root, text='Add', command=cmd_task )
btn_task.grid( row=0, column=2, padx=20 )

# Label Frame
lbl_frame = LabelFrame( root, text='Todos' )
lbl_frame.grid( row=1, column=0, columnspan=3 )

# Mark
lbl_mark = Label( lbl_frame, text='Example Text' )
lbl_mark.grid( row=0, column=0 )

root.bind( '<Return>', lambda x: cmd_task() )

cmd_show()

root.mainloop()