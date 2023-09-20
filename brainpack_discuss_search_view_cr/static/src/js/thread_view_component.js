 /** @odoo-module **/
import { ThreadView } from '@mail/components/thread_view/thread_view';
import { patch } from 'web.utils';

patch(ThreadView.prototype, 'brainpack_discuss_search_view_cr.thread_view_component', {
//     _onKeyUpSearch(ev) {
//         const query = ev.target.value.trim().toLowerCase();
//         var domain = ['|',['subject','ilike',query],['body','ilike',query]]
//         this.threadView.update({
//          stringifiedDomain: JSON.stringify(domain),
//        });
//        this.threadView._onChangeStringifiedDomain()
//    }
    _onKeyUpSearch(ev) {
        const query = ev.target.value.trim().toLowerCase()
        var domain = ['|',['subject','ilike',query],['body','ilike',query]]

        if(query != ''){
            this.threadView.update({
              searchMessage: true,
              searchString: ev.target.value,
              upDisable:false,
              downDisable:false,
            });
        }
        else{
            this.threadView.update({
              searchMessage: false,
              upDisable:true,
              downDisable:true,
              searchString: ev.target.value,
            });
        }
        this.threadView.update({
          stringifiedDomain: JSON.stringify(domain),
        });
        this.threadView._onChangeStringifiedDomain()
    },
    _onClickUp(){
        var self = this
        var nextMessage = 0
        if(this.threadView.numberOfSearch){
            nextMessage = this.threadView.currentSearchCount + 1
        }

        if(nextMessage >= this.threadView.numberOfSearch){
            this.threadView.update({
              upDisable: true,
              downDisable:false
            });
        }
        else if(nextMessage < this.threadView.numberOfSearch){
            this.threadView.update({
              downDisable: false,
            });
        }
        if(nextMessage > this.threadView.numberOfSearch){
            return false
        }

        this.threadView.update({
          currentSearchCount: nextMessage,
        });

        this.messaging.discuss.update({
          currentSearchCount: nextMessage,
        });

        if(nextMessage > 0){
            this.threadView.update({
              searchMessageId : this.threadView.threadViewer.threadCache.SearchMessages[nextMessage-1].id,
            });
        }
        else{
            this.threadView.update({
              searchMessageId : false,
            });
        }

        if(this.threadView.searchMessageId){
            setTimeout(function(){
                if($('.o_Message[data-id='+self.threadView.searchMessageId+']').length > 0){
                    $('.o_ThreadView_messageList').animate({
                        scrollTop: $('.o_Message[data-id='+self.threadView.searchMessageId+']')[0].offsetTop - 100 ,
                    }, 400);
                }
                else{
                    self.threadView.update({searchUpDown:true})
//                    $.blockUI({ message: '<h1><img class="chatter_loader" src="/brainpack_discuss_search_view_cr/static/images/imgpsh_fullsize_anim.gif" style="height:height: 150px;"/></h1>' })
                    $('.o_ThreadView').block({ message: '<h1><img class="chatter_loader" src="/brainpack_discuss_search_view_cr/static/images/imgpsh_fullsize_anim.gif" style="height:150px;"/></h1>' })
                    self.threadView.threadViewer.threadCache.loadMoreMessages();
                }
            }, 1000);
        }
    },
    _onClickDown(){
        var self = this
        var nextMessage = 0
        if(this.threadView.numberOfSearch){
            nextMessage = this.threadView.currentSearchCount - 1
            if(nextMessage == 0){
                return false
            }
            if(nextMessage == 1){
                this.threadView.update({
                  upDisable: false,
                  downDisable:true
                });
            }
            else if(nextMessage > 1){
                this.threadView.update({
                  upDisable: false,
                });
            }
        }
        this.threadView.update({
          currentSearchCount: nextMessage,
        });

        if(nextMessage > 0){
            this.threadView.update({
              searchMessageId : this.threadView.threadViewer.threadCache.SearchMessages[nextMessage-1].id,
            });
        }
        else{
            this.threadView.update({
              searchMessageId : false,
            });
        }
        if(this.threadView.searchMessageId){
            setTimeout(function(){
                if($('.o_Message[data-id='+self.threadView.searchMessageId+']').length > 0){
                    $('.o_ThreadView_messageList').animate({
                        scrollTop: $('.o_Message[data-id='+self.threadView.searchMessageId+']')[0].offsetTop - 100 ,
                    }, 200);
                }
                else{
                    self.threadView.update({searchUpDown:true})
//                    $.blockUI({ message: '<h1><img class="chatter_loader" src="/brainpack_discuss_search_view_cr/static/images/imgpsh_fullsize_anim.gif" style="height:150px;"/></h1>' })
                    $('.o_ThreadView').block({ message: '<h1><img class="chatter_loader" src="/brainpack_discuss_search_view_cr/static/images/imgpsh_fullsize_anim.gif" style="height:150px;"/></h1>' })
                    self.threadView.threadViewer.threadCache.loadMoreMessages();
                }
            }, 700);
        }
    }
});