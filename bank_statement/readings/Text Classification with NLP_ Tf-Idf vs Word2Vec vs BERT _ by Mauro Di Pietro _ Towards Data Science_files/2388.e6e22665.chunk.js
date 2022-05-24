(self.webpackChunklite=self.webpackChunklite||[]).push([[2388],{14856:(e,n,t)=>{"use strict";t.d(n,{Z:()=>a});var r=t(67294);function s(){return(s=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var t=arguments[n];for(var r in t)Object.prototype.hasOwnProperty.call(t,r)&&(e[r]=t[r])}return e}).apply(this,arguments)}var i=r.createElement("rect",{x:26.25,y:9.25,width:.5,height:6.5,rx:.25,strokeWidth:.5}),l=r.createElement("rect",{x:29.75,y:12.25,width:.5,height:6.5,rx:.25,transform:"rotate(90 29.75 12.25)",strokeWidth:.5}),o=r.createElement("path",{d:"M19.5 12.5h-7a1 1 0 0 0-1 1v11a1 1 0 0 0 1 1h13a1 1 0 0 0 1-1v-5",strokeLinecap:"round"}),u=r.createElement("path",{d:"M11.5 14.5L19 20l4-3",strokeLinecap:"round"});const a=function(e){return r.createElement("svg",s({width:38,height:38,viewBox:"0 0 38 38",fill:"none"},e),i,l,o,u)}},99033:(e,n,t)=>{"use strict";t.d(n,{DI:()=>C,nj:()=>x,oT:()=>R});var r=t(59713),s=t.n(r),i=t(63038),l=t.n(i),o=t(28655),u=t.n(o),a=t(82492),c=t.n(a),d=t(71439),b=t(46829),m=t(67294),w=t(53976),v=t(81474),f=t(32589),p=t(95760),g=t(51512),h=t(85277);function S(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function E(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?S(Object(t),!0).forEach((function(n){s()(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):S(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function V(){var e=u()(["\n  mutation fetchOrLazilyCreateNewsletterV3AndMaybeSubscribe(\n    $userId: ID!\n    $shouldSubscribeCurrentUser: Boolean\n  ) {\n    fetchOrLazilyCreateNewsletterV3AndMaybeSubscribe(\n      userId: $userId\n      shouldSubscribeCurrentUser: $shouldSubscribeCurrentUser\n    ) {\n      __typename\n      ...useNewsletterV3Subscription_newsletterV3\n    }\n  }\n  ","\n"]);return V=function(){return e},e}function y(){var e=u()(["\n  mutation unsubscribeNewsletterV3($newsletterV3Id: ID!) {\n    unsubscribeNewsletterV3(newsletterV3Id: $newsletterV3Id)\n  }\n"]);return y=function(){return e},e}function _(){var e=u()(["\n  mutation subscribeNewsletterV3($newsletterV3Id: ID!, $shouldRecordConsent: Boolean) {\n    subscribeNewsletterV3(\n      newsletterV3Id: $newsletterV3Id\n      shouldRecordConsent: $shouldRecordConsent\n    )\n  }\n"]);return _=function(){return e},e}function O(){var e=u()(["\n  fragment useNewsletterV3Subscription_newsletterV3_viewerEdge on NewsletterV3 {\n    viewerEdge {\n      id\n      isSubscribed\n    }\n  }\n"]);return O=function(){return e},e}function I(){var e=u()(["\n  fragment useNewsletterV3Subscription_user on User {\n    id\n    username\n    newsletterV3 {\n      ...useNewsletterV3Subscription_newsletterV3\n    }\n  }\n  ","\n"]);return I=function(){return e},e}function N(){var e=u()(["\n  fragment useNewsletterV3Subscription_newsletterV3 on NewsletterV3 {\n    id\n    type\n    slug\n    name\n    collection {\n      slug\n    }\n    user {\n      id\n      name\n      username\n      newsletterV3 {\n        id\n      }\n    }\n  }\n"]);return N=function(){return e},e}var C=(0,d.Ps)(N()),x=(0,d.Ps)(I(),C),P=((0,d.Ps)(O()),(0,d.Ps)(_())),T=(0,d.Ps)(y()),L=(0,d.Ps)(V(),C),R=function(e){var n=e.newsletterV3,t=e.creator,r=e.newsletterName,s=n||{},i=s.id,o=s.type,u=s.slug,a=s.collection,d=(null==n?void 0:n.user)||t,S=null!=r?r:null==n?void 0:n.name,V=m.useState(!1),y=l()(V,2),_=y[0],O=y[1],I=(0,v.T)({newsletterSlug:u,collectionSlug:null==a?void 0:a.slug,username:null==d?void 0:d.username}),N=I.viewerEdge,C=I.loading,R=(0,w.VB)({name:"enable_auto_follow_on_subscribe",placeholder:!1}),U=m.useState(!1),k=l()(U,2),M=k[0],B=k[1];m.useEffect((function(){B(!(null==N||!N.isSubscribed))}),[null==N?void 0:N.isSubscribed]);var D=(0,p.Av)(),A=(0,g.Qi)(),j=(0,h.w)();_&&D.event("newsletterV3.subscribe.error",{newsletterV3Id:i});var $=function(e,n,t){if(t){var r={id:"User:".concat(null==d?void 0:d.id),fragment:x,fragmentName:"useNewsletterV3Subscription_user"},s=e.readFragment(r);e.writeFragment(E(E({},r),{},{data:E(E({},s),{},{newsletterV3:t})}))}if(N){var i=e.readQuery({query:v.p,variables:{newsletterSlug:u,collectionSlug:null==a?void 0:a.slug,username:null==d?void 0:d.username}}),l=c()({},i,{newsletterV3:{viewerEdge:{isSubscribed:n}}});e.writeQuery({query:v.p,variables:{newsletterSlug:u||"",collectionSlug:null==a?void 0:a.slug,username:null==d?void 0:d.username},data:l})}if(n&&R){var o=e.readQuery({query:f.J4,variables:{userId:null==d?void 0:d.id}}),b=c()({},o,{user:{viewerEdge:{isFollowing:!0}}});e.writeQuery({query:f.J4,variables:{userId:(null==d?void 0:d.id)||""},data:b})}},F=(0,b.useMutation)(P,{onCompleted:function(e){var n=e.subscribeNewsletterV3;O(!n),n&&(D.event("newsletterV3.subscribeClicked",{newsletterV3Id:i,source:A}),B(!0))},update:function(e){$(e,!0)}}),z=l()(F,1)[0],G=(0,b.useMutation)(T,{onCompleted:function(e){var n=e.unsubscribeNewsletterV3;O(!n),n&&(B(!1),j({duration:"NEXTPAGE",toastStyle:"NEWSLETTER_UNSUBSCRIBE",extraParams:{newsletterName:S||null,newsletterType:o||null,unsubscribeFn:function(){return B(!1)}}}))},update:function(e){$(e,!1)}}),W=l()(G,1)[0],Q=(0,b.useMutation)(L,{onCompleted:function(e){var n=e.fetchOrLazilyCreateNewsletterV3AndMaybeSubscribe;O(!n),n&&(D.event("newsletterV3.subscribeClicked",{newsletterV3Id:n.id,source:A}),B(!0))},update:function(e,n){var t,r=E({},null===(t=n.data)||void 0===t?void 0:t.fetchOrLazilyCreateNewsletterV3AndMaybeSubscribe);$(e,!0,r)}}),q=l()(Q,1)[0];return{isSubscribed:M,hasError:_,setSubscribe:function(e){var r=arguments.length>1&&void 0!==arguments[1]&&arguments[1];O(!1),e&&!n&&null!=t&&t.id?q({variables:{userId:null==t?void 0:t.id,shouldSubscribeCurrentUser:!0}}):e&&null!=n&&n.id?z({variables:{newsletterV3Id:null==n?void 0:n.id,shouldRecordConsent:r}}):null!=n&&n.id?W({variables:{newsletterV3Id:null==n?void 0:n.id}}):O(!0)},loading:C}}},81474:(e,n,t)=>{"use strict";t.d(n,{T:()=>u,p:()=>a});var r=t(28655),s=t.n(r),i=t(46829),l=t(71439);function o(){var e=s()(["\n  query NewsletterV3ViewerEdge($newsletterSlug: ID!, $collectionSlug: ID, $username: ID) {\n    newsletterV3(\n      newsletterSlug: $newsletterSlug\n      collectionSlug: $collectionSlug\n      username: $username\n    ) {\n      ... on NewsletterV3 {\n        id\n        viewerEdge {\n          id\n          isSubscribed\n        }\n      }\n    }\n  }\n"]);return o=function(){return e},e}var u=function(e){var n,t=e.newsletterSlug,r=void 0===t?"":t,s=e.collectionSlug,l=e.username,o=(0,i.useQuery)(a,{variables:{newsletterSlug:r,collectionSlug:s,username:l},ssr:!1,skip:!r&&!l}),u=o.loading,c=o.error,d=o.data;return u?{loading:u}:c?{error:c}:{viewerEdge:null==d||null===(n=d.newsletterV3)||void 0===n?void 0:n.viewerEdge}},a=(0,l.Ps)(o())},12388:(e,n,t)=>{"use strict";t.d(n,{X:()=>z,w:()=>G});var r=t(28655),s=t.n(r),i=t(63038),l=t.n(i),o=t(71439),u=t(67294),a=t(53976),c=t(11852),d=t(50223),b=t(42933),m=t(17614),w=t(98024),v=t(51512),f=t(67297),p=t(6522),g=t(27952);function h(){var e=s()(["\n  fragment SubscribedMembershipUpsellModal_user on User {\n    id\n    name\n    imageId\n  }\n"]);return h=function(){return e},e}var S=function(e){var n=e.user,t=e.isVisible,r=e.hide,s=(0,f.v9)((function(e){return e.config.authDomain}));return(0,a.VB)({name:"enable_referred_memberships",placeholder:!1})?u.createElement(v.cW,{source:{name:"after_subscribe_membership_upsell"}},u.createElement(d.v,{isVisible:t,hide:r,withCloseButton:!0,withAnimation:!0,buttonStyle:"STRONG",buttonSize:"REGULAR",cancelText:"Not now",confirmText:"Become a member",onConfirm:function(){window.location.href=(0,g.c5p)(s)},showCancelButton:!0,isDestructiveAction:!1},u.createElement(b.x,{marginBottom:"24px"},u.createElement(c.z,{miroId:n.imageId||p.gG,alt:n.name||"",diameter:80,freezeGifs:!1})),u.createElement(b.x,{marginBottom:{xs:"8px",sm:"8px",md:"16px",lg:"16px",xl:"16px"}},u.createElement(m.F1,{scale:{xs:"S",sm:"S",md:"L",lg:"L",xl:"L"}},"You’re subscribed to get email updates. Become a member for more.")),u.createElement(b.x,{marginBottom:"32px"},u.createElement(w.F,{tag:"span",scale:{xs:"M",sm:"M",md:"L",lg:"L",xl:"L"},color:"DARKER"},"Your membership fee directly supports ",n.name," and other writers you read. Get full access to every story on Medium.")))):null},E=(0,o.Ps)(h()),V=t(99033),y=t(76532),_=t(62181),O=t(68421),I=t(55099),N=t(52862),C=t(92528),x=t(95760),P=t(6688),T=t(77180),L=t(14391),R=t(85277),U=t(8403);function k(){return(k=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var t=arguments[n];for(var r in t)Object.prototype.hasOwnProperty.call(t,r)&&(e[r]=t[r])}return e}).apply(this,arguments)}var M=u.createElement("path",{d:"M24 13l2 2 3-3.5",strokeLinecap:"round",strokeLinejoin:"round"}),B=u.createElement("path",{d:"M19.5 12.5h-7a1 1 0 0 0-1 1v11a1 1 0 0 0 1 1h13a1 1 0 0 0 1-1v-5",strokeLinecap:"round"}),D=u.createElement("path",{d:"M11.5 14.5L19 20l4-3",strokeLinecap:"round"});const A=function(e){return u.createElement("svg",k({width:38,height:38,viewBox:"0 0 38 38",fill:"none"},e),M,B,D)};var j=t(14856),$=t(51064);function F(){var e=s()(["\n  fragment UserSubscribeButton_user on User {\n    id\n    isPartnerProgramEnrolled\n    name\n    viewerEdge {\n      id\n      isFollowing\n      isUser\n    }\n    viewerIsUser\n    newsletterV3 {\n      id\n      ...useNewsletterV3Subscription_newsletterV3\n    }\n    ...useNewsletterV3Subscription_user\n    ...SubscribedMembershipUpsellModal_user\n  }\n  ","\n  ","\n  ","\n"]);return F=function(){return e},e}var z=function(e){var n=e.user,t=e.showFirstUseToolTip,r=void 0!==t&&t,s=e.showMembershipUpsellModal,i=void 0!==s&&s,o=(0,P.I)(),c=(0,T.F)(),d=(0,y.H)().value,m=(0,$.O)(!1),f=l()(m,3),p=f[0],h=f[1],E=f[2],k=n.newsletterV3,M=(0,R.w)(),B=(0,x.Av)(),D=(0,v.Lk)(),F=(0,U.PM)(),z=(0,V.oT)({newsletterV3:k,creator:n,newsletterName:n.name||void 0}),G=z.isSubscribed,W=z.hasError,Q=z.loading,q=z.setSubscribe,Y=L.T3.WRITER_SUBSCRIPTIONS_TOOLTIP,X=!(null==d||!d.dismissableFlags.includes(Y)),Z=!!(0,a.VB)({name:"enable_writer_subscription_to_all_users",placeholder:!1}),H=!!(0,a.VB)({name:"enable_referred_memberships",placeholder:!1}),J=Z&&!X&&r&&!!d&&!G,K=H&&i,ee=(0,v.P7)(F||"").susiEntry,ne=void 0===ee?"":ee,te=["newsletter_v3_promo","writer_subscription_landing"].includes(ne),re=["newsletter_v3_promo","writer_subscription_landing","subscribe_user"].includes(ne),se=K&&re&&!(null!=d&&d.mediumMemberAt)&&G&&!n.viewerIsUser&&n.isPartnerProgramEnrolled,ie=(0,$.O)(!1),le=l()(ie,3),oe=le[0],ue=le[1],ae=le[2];if(u.useEffect((function(){se?ue():ae()}),[se]),u.useEffect((function(){F&&!se&&te&&G&&M({duration:"NEXTPAGE",toastStyle:"NEWSLETTER_SUBSCRIBE",extraParams:{newsletterName:n.name,newsletterType:L.Rr.NEWSLETTER_TYPE_AUTHOR,unsubscribeFn:function(){return q(!1)}}})}),[F,G]),W||n.viewerEdge.isUser)return null;var ce=G?"OBVIOUS":"STRONG",de=function(e,n){return function(t){return{stroke:n?t.baseColor.background.normal:e,height:"36px",width:"36px"}}},be=u.createElement(I.z,{loading:Q,size:"COMPACT",buttonStyle:ce,onClick:function(){var e;d?G?q(!1):d&&d.allowEmailAddressSharingEditorWriter?q(!0,!1):h():null!==(e=n.newsletterV3)&&void 0!==e&&e.id?B.event("newsletterV3.subscribeClicked",{newsletterV3Id:n.newsletterV3.id,source:D}):B.event("user.LOSubscribeClicked",{targetUserId:n.id,source:D})},padding:"0"},G?u.createElement(A,{className:o(de(c.accentColor.fill.normal,Q))}):u.createElement(j.Z,{className:o(de(c.accentColor.background,Q))})),me=function(e){var t=e.children;return J?u.createElement(O.o,{isVisible:!Q,flag:Y,targetDistance:10,text:"You can now subscribe to get stories delivered directly to your inbox.",darkTheme:!0},t):u.createElement(N.$,{isVisible:!Q&&!G,hideOnClick:!0,noPortal:!0,mouseEnterDelay:500,mouseLeaveDelay:0,placement:"bottom",popoverRenderFn:function(){return u.createElement(b.x,{padding:"10px 12px",maxWidth:"166px"},u.createElement(w.F,{tag:"div",scale:"S",color:"DARKER"},"Subscribe to get an email whenever ",n.name," publishes."))},role:"tooltip",targetDistance:10},t)};return u.createElement(me,null,u.createElement(b.x,null,d&&u.createElement(C.Q,{onConfirm:function(){q(!0,!0)},isVisible:p,hide:E,titleText:"Confirm your subscription to ".concat(n.name),confirmText:"Confirm now",buttonStyle:"STRONG",buttonSize:"LARGE",showCancelButton:!1,withCloseButton:!1,isDestructiveAction:!1},"When you subscribe to a writer or publication, your email address will be shared with them so they can stay in contact with you outside of Medium. Opt out any time by unsubscribing in Settings."),d?be:u.createElement(_.R9,{operation:"register",newsletterV3:k,user:n,actionUrl:k?(0,g.Zul)(k.id):(0,g.lcz)(n.id),susiEntry:"subscribe_user"},be),se&&u.createElement(S,{user:n,isVisible:oe,hide:ae})))},G=(0,o.Ps)(F(),V.DI,V.nj,E)}}]);
//# sourceMappingURL=https://stats.medium.build/lite/sourcemaps/2388.e6e22665.chunk.js.map