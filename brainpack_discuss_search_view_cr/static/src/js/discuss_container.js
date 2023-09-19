 /** @odoo-module **/
import { DiscussContainer } from '@mail/components/discuss_container/discuss_container';
import { patch } from 'web.utils';

patch(DiscussContainer.prototype, 'brainpack_discuss_search_view_cr.discuss_container', {
     _onKeyUpSearch(ev) {
        const query = ev.target.value.trim().toLowerCase()
        var domain = ['|',['subject','ilike',query],['body','ilike',query]]

        if(query != ''){
            this.discuss.update({
              searchMessage: true,
              searchString: ev.target.value,
              upDisable:false,
              downDisable:false,
            });
        }
        else{
            this.discuss.update({
              searchMessage: false,
              upDisable:true,
              downDisable:true,
              searchString: ev.target.value,
            });
        }
        this.discuss.update({
          stringifiedDomain: JSON.stringify(domain),
        });
    },
    _onClickUp(){
        var self = this
        var nextMessage = 0
        if(this.discuss.threadView.numberOfSearch){
            nextMessage = this.discuss.threadView.currentSearchCount + 1
        }

        if(nextMessage >= this.discuss.threadView.numberOfSearch){
            this.discuss.threadView.update({
              upDisable: true,
              downDisable:false
            });
        }
        else if(nextMessage < this.discuss.threadView.numberOfSearch){
            this.discuss.threadView.update({
              downDisable: false,
            });
        }
        if(nextMessage > this.discuss.threadView.numberOfSearch){
            return false
        }

        this.discuss.threadView.update({
          currentSearchCount: nextMessage,
        });

        if(nextMessage > 0 && this.discuss.threadViewer.threadCache.SearchMessages[nextMessage-1]){
            this.discuss.threadView.update({
              searchMessageId : this.discuss.threadViewer.threadCache.SearchMessages[nextMessage-1].id,
            });
        }
        else{
            this.discuss.threadView.update({
              searchMessageId : false,
            });
        }

        if(this.discuss.threadView.searchMessageId){
            setTimeout(function(){
                if($('.o_Message[data-id='+self.discuss.threadView.searchMessageId+']').length > 0){
                    $('.o_ThreadView_messageList').animate({
                        scrollTop: $('.o_Message[data-id='+self.discuss.threadView.searchMessageId+']')[0].offsetTop - 100 ,
                    }, 400);
                }
                else{
                    self.discuss.threadView.update({searchUpDown:true})
                    $.blockUI({ message: '<h1><img class="chatter_loader" src="/brainpack_discuss_search_view_cr/static/images/imgpsh_fullsize_anim.gif" style="height:150px;"/></h1>' })
                    self.discuss.threadViewer.threadCache.loadMoreMessages();
                }
            }, 1000);
        }
    },
    _onClickDown(){
        var self = this
        var nextMessage = 0
        if(this.discuss.threadView.numberOfSearch){
            nextMessage = this.discuss.threadView.currentSearchCount - 1
            if(nextMessage == 0){

                return false
            }
            if(nextMessage == 1){
                this.discuss.threadView.update({
                  upDisable: false,
                  downDisable:true
                });
            }
            else if(nextMessage > 1){
                this.discuss.threadView.update({
                  upDisable: false,
                });
            }
        }
        this.discuss.threadView.update({
          currentSearchCount: nextMessage,
        });

        if(nextMessage > 0){
            this.discuss.threadView.update({
              searchMessageId : this.discuss.threadViewer.threadCache.SearchMessages[nextMessage-1].id,
            });
        }
        else{
            this.discuss.threadView.update({
              searchMessageId : false,
            });
        }
        if(this.discuss.threadView.searchMessageId){
            setTimeout(function(){
                if($('.o_Message[data-id='+self.discuss.threadView.searchMessageId+']').length > 0){
                    $('.o_ThreadView_messageList').animate({
                        scrollTop: $('.o_Message[data-id='+self.discuss.threadView.searchMessageId+']')[0].offsetTop - 100 ,
                    }, 200);
                }
                else{
                    self.discuss.threadView.update({searchUpDown:true})
                    $.blockUI({ message: '<h1><img class="chatter_loader" src="/brainpack_discuss_search_view_cr/static/images/imgpsh_fullsize_anim.gif" style="height:150px;"/></h1>' })
                    self.discuss.threadViewer.threadCache.loadMoreMessages();
                }
            }, 300);
        }
    }
});