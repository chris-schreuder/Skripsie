from flask import Flask, render_template, request, jsonify

# from code.pet import Pet
from coding.pet import Pet
from coding.audio_handler import rec

app = Flask(__name__, static_folder='static')

pet: any
context = {'name': '', 'img': '', 'neutral': True}


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/')
def reroute_home():
    main_url = request.host_url.replace("8001", "8000").replace('/', '/home')
    return render_template('home.html', main_url=main_url)


@app.route('/petsim', methods=['POST'])
def petsim():
    global pet
    global context
    name = request.form["name"]
    pet = Pet(name=name)
    context = {'name': name, 'img': pet.pet_img, 'neutral': True}
    return render_template('main.html', context=context)


@app.route('/petsim/train', methods=['POST'])
def train():
    global pet
    global context
    button = request.form['instruct_button']
    if button == '0':
        rec(pet.train_instructions[0])
        context['img'] = pet.pet_imgs[1]
    elif button == '1':
        rec(pet.train_instructions[1])
        context['img'] = pet.pet_imgs[2]
    elif button == '2':
        rec(pet.train_instructions[2])
        context['img'] = pet.pet_imgs[3]
    elif button == '3':
        rec(pet.train_instructions[3])
        context['img'] = pet.pet_imgs[4]
    elif button == '4':
        rec(pet.train_instructions[4])
        context['img'] = pet.pet_imgs[5]
    context['neutral'] = False
    return render_template('main.html', context=context)


# @app.route('/petsim/update_img')
# def update_img():
#     global pet
#     global context
#     if not context['neutral']:
#         context['neutral'] = True
#         context['img'] = pet.pet_imgs[0]
#         return jsonify({
#             "pet_img": context['img'],
#         })
#     else:
#         return jsonify({
#             "pet_img": 'skip',
#         })


@app.route('/petsim/command', methods=['POST'])
def command():
    global pet
    global context
    rec('command')
    cost, instruction = pet.interpretCommand()
    print("Alignment cost: {:.4f}".format(cost))
    print(instruction)
    if instruction == pet.train_instructions[0]:
        context['img'] = pet.pet_imgs[1]
    elif instruction == pet.train_instructions[1]:
        context['img'] = pet.pet_imgs[2]
    elif instruction == pet.train_instructions[2]:
        context['img'] = pet.pet_imgs[3]
    elif instruction == pet.train_instructions[3]:
        context['img'] = pet.pet_imgs[4]
    elif instruction == pet.train_instructions[4]:
        context['img'] = pet.pet_imgs[5]
    context['neutral'] = False
    return render_template('main.html', context=context)


@app.route('/petsim/praise', methods=['POST'])
def praise():
    global pet
    global context
    pet.savePraise()
    context['img'] = pet.pet_imgs[0]
    context['neutral'] = False
    return render_template('main.html', context=context)


if __name__ == '__main__':
    app.run(debug=True, threaded=True)