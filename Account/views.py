from django.urls import reverse_lazy
from allauth.account.views import PasswordChangeView, PasswordSetView
from django.views.generic import TemplateView


# Create your views here.

def wordStylePug(
    words=[
        *'Welcome',
        ': )',
    ],
    word_size=40,
    *kwarg,
    **kwargs,
):
    words_length = len(words)
    colors = [
        "#eb4747",
        "#ebc247",
        "#99eb47",
        "#47eb70",
        "#47ebeb",
        "#4770eb",
        "#9947eb",
        "#eb47c2",
        "#eb4747",
    ]
    particles= [
        {'left': -40, 'top': 0 },
        {'left': -53.39745959999999, 'top': 50 },
        {'left': -90, 'top': 86.60254040000001 },
        {'left': -140, 'top': 100 },
        {'left': -190, 'top': 86.60254040000001 },
        {'left': -226.6025404, 'top': 50 },
        {'left': -240, 'top': 0 },
        {'left': -226.6025404, 'top': -50 },
        {'left': -190, 'top': -86.60254040000001 },
        {'left': -140, 'top': -100 },
        {'left': -90, 'top': -86.60254040000001 },
        {'left': -53.39745959999999, 'top': -50 },
        {'left': -40, 'top': 0 },
    ]
    text_style = f"""
        .text {{
            position: absolute;
            width: { word_size }px;
            line-height: { word_size }px;
            opacity: 0;
            overflow: hidden;
        }}
        .text::after {{
            z-index: -1;
            content: '';
            display: inline-block;
            position: absolute;
            top: 0;
            left: 0;
            width: 0;
            height: { word_size }px;
        }}
    """
    frame_style = f"""
        .frame {{
              position: absolute;
              width: { word_size }px;
              height: { word_size }px;
              border-radius: 50%;
              opacity: 0;
        }}
    """
    
    background_tags = """
    """
    text_tags = """
    """
    text_after_animation_style = """
    """
    text2_animation_style = """
    """
    frame_tags = """
    """
    particles_tags = """
    """
    particles_style = """
    """
    for index, word in enumerate(words):
        left = (index*word_size)-(words_length*word_size/2)
        text_style += f"""
            .text{ index } {{
              left: { left }px;
              top: 0;
              -webkit-animation: text-animation 1s ease-in-out { index*0.2+1 }s 1 normal forwards, text2-animation{ index } 2s ease-in-out 5s 1 normal forwards;
                      animation: text-animation 1s ease-in-out { index*0.2+1 }s 1 normal forwards, text2-animation{ index } 2s ease-in-out 5s 1 normal forwards;
            }}
            .text{ index }::after {{
              -webkit-animation: text-after-animation{ index } 2s ease-in-out 3s 1 normal forwards;
                      animation: text-after-animation{ index } 2s ease-in-out 3s 1 normal forwards;
            }}
        """
        text_after_animation_style += f"""
            @-webkit-keyframes text-after-animation{ index } {{
              0% {{
                width: 0px;
                background-color: { colors[index]};
                opacity: 1;
             }}
              50% {{
                width: 40px;
                opacity: 1;
              }}
              100% {{
                left: 40px;
                opacity: 0;
              }}
            }}
            @keyframes text-after-animation{ index } {{
              0% {{
                width: 0px;
                background-color: { colors[index] };
                opacity: 1;
              }}
              50% {{
                width: 40px;
                opacity: 1;
              }}
              100% {{
                left: 40px;
                opacity: 0;
              }}
            }}
        """
        text2_animation_style += f"""
            @-webkit-keyframes text2-animation{ index } {{
              0% {{
                left: { left }px;
                opacity: 1; 
                { "transform: scale(1, 1);" if (index == words_length-1) else "" }
              }}
              50% {{
                left: { left-word_size }px;
                opacity: 0; 
                { "transform: scale(1, 1);" if (index == words_length-1) else "" }
              }}

              { "65% {{ top: 0; transform: scale(1, 1); }}  70% {{ transform: scale(3, 3) rotate(90deg); top: -30px; }} 75% {{ left: 180px; top: 0;  opacity: 1; transform: scale(2, 2) rotate(90deg); }} 85% {{ left: 180px; }} " if (index == words_length-1) else "" } 
              
              100% {{
                left: { 1000 if (index == words_length-1) else index*40-100 }px;
                opacity: 0;
                { "transform: scale(2, 2) rotate(90deg);" if (index == words_length-1) else "" }
              }}
            }}
            
            @-webkit-keyframes text2-animation{ index } {{
              0% {{
                left: { left }px;
                opacity: 1; 
                { "transform: scale(1, 1);" if (index == words_length-1) else "" }
              }}
              50% {{
                left: { left-word_size }px;
                opacity: 0; 
                { "transform: scale(1, 1);" if (index == words_length-1) else "" }
              }}

                { "65% {{ top: 0; transform: scale(1, 1); }}  70% {{ transform: scale(3, 3) rotate(90deg); top: -30px; }} 75% {{ left: 180px; top: 0;  opacity: 1; transform: scale(2, 2) rotate(90deg); }} 85% {{ left: 180px; }} " if (index == words_length-1) else "" } 
              
              100% {{
                left: left: { 1000 if (index == words_length-1) else index*40-100 }px;
                opacity: 0;
                { "transform: scale(2, 2) rotate(90deg);" if (index == words_length-1) else "" }
              }}
            }}
        """
        ### BackGround
        background_tags += f"""        
          <div
              class='background'
              style='
              left: { index*100/words_length }%;
              height: 100vh;
              background-color: { colors[index] };
              '
          ></div>
        """
        ### Text Tages
        text_tags += f"""
            <div class='text text{ index }'>{ word }</div>
        """
        ### Frame Tages
        frame_tags += f"""
            <div
                class='frame'
                style='
                left: { index*40-(words_length*word_size/2) }px;
                top: 0;
                background-color: { colors[index] };
                -webkit-animation: frame-animation 1s ease-in-out { index*200 }ms 1 normal forwards;
                        animation: frame-animation 1s ease-in-out { index*200 }ms 1 normal forwards;
                '
            ></div>
        """
        ### Particles Loop
        for particle_index, particle in enumerate(particles) :
          particles_tags += f"""
              <div
                class='particle'
                style='
                  left: { left }px;
                  opacity: 0;
                  background-color: { colors[index] };
                  -webkit-animation: particle-animation{ index}{ particle_index } 1s ease-in-out { index*0.2+1 }s 1 normal forwards;
                          animation: particle-animation{ index}{ particle_index } 1s ease-in-out { index*0.2+1 }s 1 normal forwards;
                '
              ></div>
          """
          particles_style += f"""
              @-webkit-keyframes particle-animation{ index }{ particle_index } {{
                0% {{
                  left: { left }px;
                  top: 0;
                  opacity: 0;
                  transform: scale(1, 1);
                }}
                100% {{
                  left: { index*word_size+particle["left"] }px;
                  top: { particle["top"] }px;
                  opacity: 1;
                  transform: scale(0, 0);
                }}
              }}
              @keyframes particle-animation{ index }{ particle_index } {{
                0% {{
                  left: { left }px;
                  top: 0;
                  opacity: 0;
                  transform: scale(1, 1);
                }}
                100% {{
                  left: { index*word_size+particle["left"] }px;
                  top: { particle["top"] }px;
                  opacity: 1;
                  transform: scale(0, 0);
                }}
              }}
          """
    return {
      "text_style": text_style,
      "frame_style": frame_style,
      "particles_style": particles_style,
      "background_tags": background_tags,
      "text_tags": text_tags,
      "frame_tags": frame_tags,
      "particles_tags": particles_tags,
    }


class SplashView(TemplateView):
    template_name = "Splash/logo.html"
    # context_object_name = 'splash_word'

    # def get_context_data(self, **kwargs):
    #     # # Call the base implementation first to get the context
    #     context = super(SplashView, self).get_context_data(**kwargs)
    #     # # Create any data and add it to the context
    #     # words = [
    #     #     *'Welcome',
    #     #     ': )',
    #     # ]
    #     # word_size = 40
    #     # colors = [
    #     #     "#eb4747",
    #     #     "#ebc247",
    #     #     "#99eb47",
    #     #     "#47eb70",
    #     #     "#47ebeb",
    #     #     "#4770eb",
    #     #     "#9947eb",
    #     #     "#eb47c2",
    #     #     "#eb4747",
    #     # ]
        
    #     # context['word_size'] = word_size
    #     # context['words_data'] = list(
    #     #     map(
    #     #         lambda x: {
    #     #             'word': x[1],
    #     #             'bg_color': colors[x[0]],
    #     #             'bg_left': x[0]*100/len(words),
    #     #             'left': x[0]*word_size-140,
    #     #             'left2': x[0]*word_size-100,
    #     #             'fram_ms': x[0]*200,
    #     #             'text_s': x[0]*0.2+1,
    #     #             'particles': [
    #     #                 {'left': x[0]*word_size-40, 'top': 0, 'index': 0 },
    #     #                 {'left': x[0]*word_size-53.39745959999999, 'top': 50, 'index': 1 },
    #     #                 {'left': x[0]*word_size-90, 'top': 86.60254040000001, 'index': 2 },
    #     #                 {'left': x[0]*word_size-140, 'top': 100, 'index': 3 },
    #     #                 {'left': x[0]*word_size-190, 'top': 86.60254040000001, 'index': 4 },
    #     #                 {'left': x[0]*word_size-226.6025404, 'top': 50, 'index': 5 },
    #     #                 {'left': x[0]*word_size-240, 'top': 0, 'index': 6 },
    #     #                 {'left': x[0]*word_size-226.6025404, 'top': -50, 'index': 7 },
    #     #                 {'left': x[0]*word_size-190, 'top': -86.60254040000001, 'index': 8 },
    #     #                 {'left': x[0]*word_size-140, 'top': -100, 'index': 9 },
    #     #                 {'left': x[0]*word_size-90, 'top': -86.60254040000001, 'index': 10 },
    #     #                 {'left': x[0]*word_size-53.39745959999999, 'top': -50, 'index': 11 },
    #     #                 {'left': x[0]*word_size-40, 'top': 0, 'index': 12 },
    #     #             ],
    #     #         },
    #     #         enumerate(words),
    #     #     )
    #     # )
    #     wordStyle = wordStylePug()
    #     context['text_style'] = wordStyle["text_style"]
    #     context['frame_style'] = wordStyle["frame_style"]
    #     context['particles_style'] = wordStyle["particles_style"]
    #     context['background_tags'] = wordStyle["background_tags"]
    #     context['text_tags'] = wordStyle["text_tags"]
    #     context['frame_tags'] = wordStyle["frame_tags"]
    #     context['particles_tags'] = wordStyle["particles_tags"]
    #     return context


## from Velzon

class MyPasswordChangeView( PasswordChangeView):
    success_url = reverse_lazy("dashboards:dashboard")


class MyPasswordSetView( PasswordSetView):
    success_url = reverse_lazy("dashboards:dashboard")